import re
from typing import List
from unittest import result
from constants import BENCHMARKS
from ddl import Index
from parse_log import parse_sql_log, process_queries
from postgres import Postgres
from util import get_ddl_for_benchmark, get_logger

logger = get_logger("explain")


def explain_query_with_costs(postgres: Postgres, query: str):
    explain_query = f"EXPLAIN {query}"
    results = postgres.execute(explain_query)
    # There's only a single row of results with the root level result appearing in the first index.
    root_level_results = results[0][0]

    float_regex = r"[0-9]*[.][0-9]+"  # A hacky regex for floating points
    cost_regex = f"cost\=({float_regex})\.\.({float_regex})"
    matches = re.search(cost_regex, root_level_results)

    assert matches, "No matches for cost found"
    min_cost = matches.group(1)
    max_cost = matches.group(2)

    logger.info(max_cost)
    return max_cost


def create_hypopg_index(postgres: Postgres, index: Index):
    column_list_str = ", ".join(index.columns)
    create_index_sql = (
        f"CREATE INDEX IF NOT EXISTS {index.name} ON {index.table} ({column_list_str});"
    )
    hypopg_query = f"SELECT * FROM hypopg_create_index('{create_index_sql}')"

    # TODO: Add some error handling here.
    postgres.execute(hypopg_query)
    return


def drop_hypopg_index(postgres: Postgres, index: Index):
    # We must first fetch the index OID
    select_sql = f"SELECT indexrelid, index_name FROM hypopg_list_indexes WHERE index_name LIKE '%{index.name}';"
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


def identify_workload(workload_csv: str) -> List[str]:
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
    return identified_workloads


db = Postgres()
db.connect()

index = Index("review_i_id", table="review", columns=["i_id"])
create_hypopg_index(db, index)
explain_query_with_costs(db, "SELECT avg(rating) FROM review r WHERE r.i_id=9212")
drop_hypopg_index(db, index)

# identify_workload("/home/kramana2/postgresql/data/bd95fb52-da3c-49a0-823f-58c8b0424d3b/copy-postgresql-2022-03-14_005706.csv")

drop_all_indexes(db)
