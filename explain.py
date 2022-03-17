import itertools
import json
import os
from pathlib import Path
import re
import traceback
from typing import List, Mapping, Tuple
from unittest import result
from constants import (
    ACTIONS_SQL,
    BENCHMARKS,
    EPINIONS,
    RESULTS_DIRECTORY,
    STATE_CANDIDATES,
    STATE_JSON,
    TEMP_CSV,
)
from ddl import Index
from parse_log import parse_sql_log, process_queries
from postgres import Postgres
from results import parse_run_data
from util import (
    combine_csvs,
    construct_index_name,
    get_ddl_for_benchmark,
    get_logger,
    index_list_to_dict_list,
    print_indexes,
)

logger = get_logger("explain")


def explain_query_with_costs(postgres: Postgres, query: str) -> float:
    explain_query = f"EXPLAIN {query}"
    results = postgres.execute(explain_query)
    # There's only a single row of results with the root level result appearing in the first index.
    root_level_results = results[0][0]

    float_regex = r"[0-9]*[.][0-9]+"  # A hacky regex for floating points
    cost_regex = f"cost\=({float_regex})\.\.({float_regex})"
    matches = re.search(cost_regex, root_level_results)

    assert matches, "No matches for cost found"
    min_cost = round(float(matches.group(1)), 2)
    max_cost = round(float(matches.group(2)), 2)

    return max_cost


def _get_create_index_command(index: Index) -> str:
    column_list_str = ", ".join(index.columns)
    return f"CREATE INDEX IF NOT EXISTS {index.name} ON {index.table} USING {index.itype} ({column_list_str});"


def create_hypopg_index(postgres: Postgres, index: Index):
    """
    Creates a HypoPG index.
    """
    hypopg_query = (
        f"SELECT * FROM hypopg_create_index('{_get_create_index_command(index)}')"
    )

    # TODO: Add some error handling here.
    postgres.execute(hypopg_query)
    postgres.commit()
    return


def drop_hypopg_index(postgres: Postgres, index: Index):
    """
    Drops a HypoPG index.
    """
    # We must first fetch the index OID
    # Names of HypoPG indexes are width constrained. Hack past that
    select_sql = f"SELECT indexrelid, index_name FROM hypopg_list_indexes WHERE index_name LIKE '%{index.name[:48]}%';"
    results = postgres.execute(select_sql)

    assert len(results) == 1, f"Incorrect number ({len(results)}) returned"
    index_relid = results[0][0]
    index_name = results[0][1]  # This is the name under which HypoPG saves the index.

    logger.warning(f"Dropping HypoPG index: {index_name}")
    drop_index_sql = f"SELECT * FROM hypopg_drop_index({index_relid});"
    # TODO: Add some error handling here.
    postgres.execute(drop_index_sql)

    results = postgres.execute(select_sql)
    assert len(results) == 0, f"Index {index_name} not dropped"


def _get_drop_index_command(index_name: str) -> str:
    """
    Returns the command for dropping an index.
    """
    return f"DROP INDEX IF EXISTS {index_name};"


def drop_index(postgres: Postgres, index_name: str):
    """
    Drops the given REAL index.
    """
    sql = _get_drop_index_command(index_name)

    logger.info(f"Dropping index: {index_name}")
    postgres.execute(sql)
    postgres.commit()

    return


def drop_all_indexes(postgres: Postgres, read_only=False) -> List[str]:
    """
    Drops all droppable indexes.
    """
    sql = """
    SELECT indexrelid,
       subq.relname,
       indisunique,
       indisprimary,
       indisexclusion
    FROM   pg_index
        JOIN (SELECT oid,
                     relname
                FROM   pg_class
                WHERE  relname IN (SELECT indexname
                                    FROM   pg_indexes
                                    WHERE  schemaname = 'public')) AS subq
            ON indexrelid = subq.oid
    WHERE  NOT ( indisunique
                OR indisprimary
                OR indisexclusion );
    """

    results = postgres.execute(sql)

    if not results:
        logger.info("No indexes to drop, we're all good")
        return []

    indexes = [index_row[1] for index_row in results]

    if not read_only:
        for index in indexes:
            drop_index(postgres, index)

    return indexes


def run_vacuum(postgres: Postgres):
    """
    Runs vacuuming on the Postgres instance.
    """
    postgres.execute("VACUUM;")


def identify_workload(workload_csv: str) -> Tuple[List[str], Mapping[str, int]]:
    """
    Identifies the reference workloads in the log file.
    """
    # Parse the CSV log file
    query_frequency = parse_sql_log(workload_csv)
    identified_workloads = []

    # Load all the DDLs first
    ddl_map = {}
    for benchmark in BENCHMARKS:
        ddl_map[benchmark] = get_ddl_for_benchmark(benchmark)

        # Now attempt to interpret the queries with knowledge of DDL
        freqs = process_queries(ddl_map[benchmark], query_frequency)
        if not freqs["column_access"]:
            logger.info(f"Workload does not contain DDL: {benchmark}")
            continue

        freqs["query"] = query_frequency
        identified_workloads.append({"benchmark": benchmark, "frequencies": freqs})

    assert identified_workloads, "Could not identify workload"

    workloads = [w["benchmark"] for w in identified_workloads]
    logger.info(f"Identified workloads: {workloads}")
    return identified_workloads


def get_hypopg_workload_cost_with_indexes(
    postgres: Postgres, indexes: List[Index], query_freq: Mapping[str, int]
) -> float:
    """
    Computes the EXPLAIN costs of running the workload against the set of candidate indexes.
    """
    # 2. Let's create the requested indexes.
    for index in indexes:
        create_hypopg_index(postgres, index)
    postgres.commit()

    # 3. Run vacuuming as a precautionary step.
    # run_vacuum(postgres)

    cost = 0
    for query in query_freq:
        cost += (explain_query_with_costs(postgres, query)) * query_freq[query]

    logger.info(f"Total cost: {cost}")

    # 4. Finally, drop all indexes.
    for index in indexes:
        drop_hypopg_index(postgres, index)

    return round(cost, 2)


def expand_candidate_indexes(indexes: List[List[Index]]):
    # We know the frequency with which each column is accessed.
    # 1. Expand the columns explored.

    # 2. Expand the number of columns per index.

    # 3. Expand by the type of index (this ought to depend on the profile)
    pass


def generate_candidate_indexes(benchmark, workload_data):
    ddl = get_ddl_for_benchmark(benchmark)

    N_CANDIDATE_COLUMNS = 10
    N_COMBOS = 10
    N_MULTI_COMBOS = 20

    column_importance = workload_data["column_importance"]

    # Cache the name of the columns to the name of the table
    column_cache = {}
    for column in column_importance:
        parts = column.split(".")
        table_name, column_name = parts[0], parts[1]
        column_cache[column] = (table_name, column_name)

    # Let's sort the columns by "importance" chucking away the importance values
    column_importance_list = [
        (key, value) for (key, value) in column_importance.items()
    ]
    column_importance_list.sort(key=lambda x: x[1], reverse=True)
    N_CANDIDATE_COLUMNS = min(len(column_importance_list), N_CANDIDATE_COLUMNS)
    column_importance_list = column_importance_list[:N_CANDIDATE_COLUMNS]
    column_importance_list = [x[0] for x in column_importance_list]

    # Similarly, let's process the query templates.
    query_templates = workload_data["query_templates"]
    query_template_list = [(key, value) for (key, value) in query_templates.items()]
    query_template_list.sort(key=lambda x: x[1], reverse=True)
    N_COMBOS = min(len(query_template_list), N_COMBOS)
    query_template_list = query_template_list[:N_COMBOS]
    query_template_list = [x[0] for x in query_template_list]

    candidate_indexes = []
    # Single column indexes
    single_col_indexes = []
    for column in column_importance_list:
        parts = column.split(".")
        table_name, column_name = parts[0], parts[1]
        index_name = construct_index_name(table_name, [column_name])
        single_col_indexes.append([Index(index_name, table_name, [column_name])])
        logger.info(f"Candidate single column: {index_name}")

    # Two column indexes.
    two_col_indexes = []
    for template in query_template_list:
        combinations = itertools.combinations(template, r=2)
        for combo in combinations:
            col1 = combo[0]
            col2 = combo[1]
            if column_cache[col1][0] == column_cache[col2][0]:
                col1_name = column_cache[col1][1]
                col2_name = column_cache[col2][1]
                table_name = column_cache[col1][0]
                index_name = construct_index_name(table_name, [col1_name, col2_name])
                two_col_indexes.append(
                    [Index(index_name, table_name, [col1_name, col2_name])]
                )

                logger.info(f"Candidate two columns: {index_name}")

    # Three column indexes
    # Same spiel as two column indexes.
    three_col_indexes = []
    for template in query_template_list:
        combinations = itertools.combinations(template, r=3)
        for combo in combinations:
            col1 = combo[0]
            col2 = combo[1]
            col3 = combo[2]

            if (
                column_cache[col1][0] == column_cache[col2][0]
                and column_cache[col1][0] == column_cache[col3][0]
            ):
                col1_name = column_cache[col1][1]
                col2_name = column_cache[col2][1]
                col3_name = column_cache[col3][1]
                table_name = column_cache[col1][0]
                index_name = construct_index_name(
                    table_name, [col1_name, col2_name, col3_name]
                )
                three_col_indexes.append(
                    [Index(index_name, table_name, [col1_name, col2_name, col3_name])]
                )

                logger.info(f"Candidate three columns: {index_name}")

    first_pass_candidates = []
    first_pass_candidates.extend(single_col_indexes)
    first_pass_candidates.extend(two_col_indexes)
    first_pass_candidates.extend(three_col_indexes)

    # Now, generate valid combinations of these indexes.
    # Looking at you, indexjungle.
    multi_candidate_indexes = []
    raw_candidates = [index_list[0] for index_list in first_pass_candidates]
    combinations = []
    combinations.extend(itertools.combinations(raw_candidates, r=2))
    combinations.extend(itertools.combinations(raw_candidates, r=3))

    # Filter out the valid combos rather aggressively
    for combo in combinations:
        # If a column occurs twice, the combo is ineligible.
        column_accesses = {}
        ineligible = False
        for index in combo:
            for col in index.columns:
                if col in column_accesses.get(index.table, []):
                    ineligible = True
                    break

                column_accesses[index.table] = column_accesses.get(index.table, [])
                column_accesses[index.table].append(col)

            if ineligible:
                break

        if not ineligible:
            multi_candidate_indexes.append(list(combo))

    # Next, rank the multicolumn indexes by importance
    multi_candidate_indexes_list = []
    multi_candidate_avg_indexes_list = []
    for index_list in multi_candidate_indexes:
        imp = 0
        num_cols = 0
        for index in index_list:
            for col in index.columns:
                imp += column_importance[f"{index.table}.{col}"]
                num_cols += 1

        avg_imp = round((imp / num_cols), 2)
        logger.info(
            f"Importance: {imp} \t Average imp: {avg_imp}  Multi column indexes: {print_indexes(index_list)}"
        )
        multi_candidate_indexes_list.append((index_list, imp))
        multi_candidate_avg_indexes_list.append((index_list, avg_imp))

    # Now, sort by importance
    multi_candidate_indexes_list.sort(key=lambda x: x[1], reverse=True)
    multi_candidate_avg_indexes_list.sort(key=lambda x: x[1], reverse=True)

    N_MULTI_COMBOS = min(len(multi_candidate_indexes_list), N_MULTI_COMBOS)
    multi_candidate_indexes_list = multi_candidate_indexes_list[:N_MULTI_COMBOS]
    multi_candidate_avg_indexes_list = multi_candidate_avg_indexes_list[:N_MULTI_COMBOS]

    multi_candidate_indexes = [x[0] for x in multi_candidate_indexes_list]
    multi_candidate_indexes.extend([x[0] for x in multi_candidate_avg_indexes_list])

    for index_list in multi_candidate_indexes:
        logger.info(f"Multi column indexes: {print_indexes(index_list)}")

    # Pay careful attention to the order.
    # We want indexes with the highest probabilities going first.
    candidate_indexes.extend(multi_candidate_indexes)
    candidate_indexes.extend(three_col_indexes)
    candidate_indexes.extend(two_col_indexes)
    candidate_indexes.extend(single_col_indexes)
    return candidate_indexes


def remove_duplicates(candidate_indexes: List[List[Index]]) -> List[List[Index]]:
    cache = {}
    for index_list in candidate_indexes:
        pass


def write_out_indexes(
    indexes: List[Index],
    index_cost: float,
    indexes_to_drop: List[str],
    action_sql: str,
    state_json: str = STATE_JSON,
):
    """
    Write out the indexes to the given action file while maintaining state.
    This helps when we're running against a timer in order to maintain state.
    """
    with open(action_sql, "w") as sql_file:
        with open(str(state_json), "w") as json_file:
            # TODO: We need to write out index drops as well.
            index_state = {
                "indexes": index_list_to_dict_list(indexes),
                "cost": index_cost,
            }

            sql_lines = []
            create_lines = []
            for index in indexes:
                create_lines.append(_get_create_index_command(index) + "\n")

            # Get the SQL Commands for indexes to drop.
            drop_sql_lines = []
            for index in indexes_to_drop:
                drop_sql_lines.append(_get_drop_index_command(index) + "\n")

            # Finally, write out the SQL
            sql_lines.extend(drop_sql_lines)
            sql_lines.extend(create_lines)

            sql_file.writelines(sql_lines)
            json.dump(index_state, json_file)


def persist_candidate_indexes(
    candidate_indexes: List[Index], state_file: Path = STATE_CANDIDATES
):
    """
    Persists the indexes to be tried next.
    """
    # Flip over the indexes
    indexes = candidate_indexes[:]
    indexes.reverse()

    with open(str(state_file), "w") as fp:
        lines = []
        for index_list in indexes:
            index_dict = index_list_to_dict_list(index_list)
            lines.append(json.dumps(index_dict) + "\n")

        fp.writelines(lines)


def get_exploration_state(state_file: Path = STATE_CANDIDATES) -> List[List[Index]]:
    if not state_file.exists():
        return []

    # File exists, read line by line
    candidate_indexes = []
    with open(state_file, "r") as fp:
        for line in fp:
            json_data = json.loads(line)
            index_list = []
            for index in json_data:
                index_list.append(Index(**index))
            candidate_indexes.append(index_list)

    candidate_indexes.reverse()
    return candidate_indexes


def remove_candidate_tail(state_file: Path = STATE_CANDIDATES):
    """
    The candidates file is used to maintain state across iterations.
    This function updates the file after each candidate is tested.
    """
    num_lines_cmd = f"sed -n '$=' {str(STATE_CANDIDATES)}"

    if not STATE_CANDIDATES.exists():
        # Nothing to do here, return.
        return

    num_lines = int(os.popen(num_lines_cmd).read().strip())
    if num_lines == 1:
        # Remove the file
        os.remove(STATE_CANDIDATES)
        return

    # Multiple lines left.
    strip_last_line = f"sed -i '$ d' {str(STATE_CANDIDATES)}"
    os.popen(strip_last_line)


def index_runner(workload_csv: str, action_sql: str = ACTIONS_SQL):
    # First things first, let's create the DB handle.
    db = Postgres()
    db.connect()

    # Let's assert that the CSV file actually exists.
    assert Path(workload_csv).exists(), "Supplied input file does not exist"

    # For the evaluation, we're told that we'll be supplied exactly one workload.
    # So there are no mixes.
    # Parse the workload queries as a one-time activity

    workloads_w_data = identify_workload(workload_csv)
    workload = workloads_w_data[0]
    target_benchmark = workload["benchmark"]
    query_frequency = workload["frequencies"]["query"]

    # 1. Let's drop all indexes.
    indexes_to_drop = drop_all_indexes(db, read_only=False)
    # This must also be cataloged in the Actions SQL file to persist
    # through DB restores.

    candidate_indexes = get_exploration_state()
    mid_run = None
    if candidate_indexes:
        mid_run = True
    else:
        mid_run = False

    if not mid_run:
        candidate_indexes = generate_candidate_indexes(
            target_benchmark, workload["frequencies"]
        )

    # Generate a set of candidate indexes.
    # Note each element is a set of indexes.
    if not mid_run:
        indexes_dict_list = parse_run_data(target_benchmark, RESULTS_DIRECTORY)
        for index_list in indexes_dict_list:
            candidate_indexes.append([Index(**index) for index in index_list])

    persist_candidate_indexes(candidate_indexes)
    # TODO: Remove indexes that are repeating

    # Run once, without any indexes.
    no_index_cost = get_hypopg_workload_cost_with_indexes(db, [], query_frequency)

    costs = []
    best_indexes = []  # ie. No index.
    best_cost = no_index_cost

    for index_list in candidate_indexes:
        logger.info(f"Running EXPLAIN against indexes: {print_indexes(index_list)}")
        cost = get_hypopg_workload_cost_with_indexes(db, index_list, query_frequency)

        costs.append((index_list, cost))

        # If cost is better
        if cost < best_cost:
            best_indexes = index_list
            best_cost = cost
            # Write this out, because you may get interrupted by the timer.
            write_out_indexes(best_indexes, best_cost, indexes_to_drop, action_sql)

        # Finally, remove the candidate from the potential list of candidates
        remove_candidate_tail()

    # This is for our own consumption.
    costs.sort(key=lambda x: x[-1], reverse=False)
    costs = costs[:5]  # Best 5 candidates

    logger.info("BEST INDEXES!!")
    for cost in costs:
        logger.info(f"Cost: {cost[1]} \t Index: {print_indexes(cost[0])}")

    logger.info("NO INDEX!!")
    logger.info(f"Cost: {no_index_cost} \t Index: {[]}")

    db.disconnect()

    return


# Epinions
workload_csv = "/home/kramana2/postgresql/data/bd95fb52-da3c-49a0-823f-58c8b0424d3b/copy-postgresql-2022-03-14_005706.csv"

# index_runner(workload_csv, "actions.sql")

# Indexjungle
# combine_csvs(
#     [
#         "/home/kramana2/postgresql/data/f240c871-e280-4aea-8b16-b69d09dcea30/postgresql-2022-03-14_090644.csv",
#         "/home/kramana2/postgresql/data/f240c871-e280-4aea-8b16-b69d09dcea30/postgresql-2022-03-14_090732.csv",
#         "/home/kramana2/postgresql/data/f240c871-e280-4aea-8b16-b69d09dcea30/postgresql-2022-03-14_090816.csv",
#         "/home/kramana2/postgresql/data/f240c871-e280-4aea-8b16-b69d09dcea30/postgresql-2022-03-14_090902.csv"
#     ]
# )

# Timeseries
# "/home/kramana2/postgresql/data/92319816-05bf-488c-bb54-b75fe2fcf645/postgresql-2022-03-14_064300.csv"

# index_runner(str(TEMP_CSV))
# index_runner("epinions.csv")

index_runner(
    "/home/kramana2/postgresql/data/f240c871-e280-4aea-8b16-b69d09dcea30/postgresql-2022-03-14_090732.csv"
)
