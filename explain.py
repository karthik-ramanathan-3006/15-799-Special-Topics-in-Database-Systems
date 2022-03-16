from pathlib import Path
import re
from typing import List, Mapping, Tuple
from unittest import result
from constants import ACTIONS_SQL, BENCHMARKS, EPINIONS, RESULTS_DIRECTORY, TEMP_CSV
from ddl import Index
from parse_log import parse_sql_log, process_queries
from postgres import Postgres
from results import parse_run_data
from util import combine_csvs, get_ddl_for_benchmark, get_logger, print_indexes

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
    hypopg_query = f"SELECT * FROM hypopg_create_index('{_get_create_index_command(index)}')"

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


def drop_index(postgres: Postgres, index_name: str):
    """
    Drops the given REAL index.
    """
    sql = f"DROP INDEX IF EXISTS {index_name}"

    logger.info(f"Dropping index: {index_name}")
    postgres.execute(sql)
    postgres.commit()

    return


def drop_all_indexes(postgres: Postgres):
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
        return

    for index_row in results:
        drop_index(postgres, index_row[1])

    return


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
        column_access_frequency = process_queries(ddl_map[benchmark], query_frequency)
        if not column_access_frequency:
            logger.info(f"Workload does not contain DDL: {benchmark}")
            continue

        identified_workloads.append(benchmark)

    assert identified_workloads, "Could not identify workload"

    logger.info(f"Identified workloads: {identified_workloads}")
    return (identified_workloads, query_frequency)


def get_hypopg_workload_cost_with_indexes(postgres: Postgres, indexes: List[Index], query_freq: Mapping[str, int]) ->float:
    """
    Computes the EXPLAIN costs of running the workload against the set of candidate indexes. 
    """
    # 1. Let's drop all indexes.
    drop_all_indexes(postgres)

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


def index_runner(workload_csv: str, action_sql: str = ACTIONS_SQL):
    # First things first, let's create the DB handle.
    db = Postgres()
    db.connect()

    # Let's assert that the CSV file actually exists.
    assert Path(workload_csv).exists(), "Supplied input file does not exist"

    # For the evaluation, we're told that we'll be supplied exactly one workload.
    # So there are no mixes.
    # Parse the workload queries as a one-time activity

    (workloads, query_frequency) = identify_workload(workload_csv)
    target_benchmark = workloads[0]

    # Generate a set of candidate indexes.
    # Note each element is a set of indexes.
    candidate_indexes = parse_run_data(target_benchmark, RESULTS_DIRECTORY)

    # Expand the candidate indexes.

    costs = []
    for index_list in candidate_indexes:
        indexes = [Index(**index) for index in index_list]
        logger.info(f"Running EXPLAIN against indexes: {print_indexes(indexes)}")
        cost = get_hypopg_workload_cost_with_indexes(db, indexes, query_frequency)

        costs.append((indexes, cost))
    
    costs.sort(key=lambda x: x[-1], reverse=False) 
    costs = costs[:5] # Best 5 candidates
    
    logger.info("BEST INDEXES!!")
    for cost in costs:
        logger.info(f"Cost: {cost[1]} \t Index: {print_indexes(cost[0])}")
    
    logger.info("NO INDEX!!")
    cost = get_hypopg_workload_cost_with_indexes(db, [], query_frequency)
    logger.info(f"Cost: {cost} \t Index: {[]}")


    # Write out to the actions.SQL file
    with open(action_sql, "w") as sql_file:
        # TODO: We need to write out index drops as well.
        (best_indexes, _) = costs[0]

        sql_lines = []
        for index in best_indexes:
            sql_lines.append(_get_create_index_command(index) + "\n")


        # Finally, write out the SQL
        sql_file.writelines(sql_lines)

    db.disconnect()


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

index_runner(str(TEMP_CSV))
