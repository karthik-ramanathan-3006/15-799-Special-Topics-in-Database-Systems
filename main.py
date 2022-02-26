import argparse
import csv
import logging
import pglast
import sql_metadata
import sqlparse
from constants import WHERE_CLAUSE

from ddl import DDL
from postgres import Postgres

logging.basicConfig()
logger = logging.getLogger("15-799")
logger.setLevel(logging.DEBUG)

# Source: https://www.postgresql.org/docs/14/runtime-config-logging.html#RUNTIME-CONFIG-LOGGING-CSVLOG
CSV_LOG_KEYS = [
    "log_time",  # timestamp(3) with time zone,
    "user_name",  # text,
    "database_name",  # text,
    "process_id",  # integer,
    "connection_from",  # text,
    "session_id",  # text,
    "session_line_num",  # bigint,
    "command_tag",  # text,
    "session_start_time",  # timestamp with time zone,
    "virtual_transaction_id",  # text,
    "transaction_id",  # bigint,
    "error_severity",  # text,
    "sql_state_code",  # text,
    "message",  # text,
    "detail",  # text,
    "hint",  # text,
    "internal_query",  # text,
    "internal_query_pos",  # integer,
    "context",  # text,
    "query",  # text,
    "query_pos",  # integer,
    "location",  # text,
    "application_name",  # text,
    "backend_type",  # text,
    "leader_pid",  # integer,
    "query_id",  # bigint,
    # PRIMARY KEY (session_id, session_line_num)
]

# Command tags whose logs we ignore
EXCLUDE_COLLECTION = [
    "BEGIN",
    "COMMIT",
]


def row_as_str(row_array):
    return ", ".join(row_array)


def process_queries(ddl: DDL, query_frequency):
    table_access_frequency = {}
    column_access_frequency = {}

    # Things to account for:
    # 1. Query type: SELECT vs UPDATE vs INSERT
    # 2. WHERE CLAUSE and order of columns
    # 3. Subqueries:
    # 4. LIMIT and offset
    # 5. JOIN clauses (a.colA v b.colA)
    # 6. Clean out values from WHERE clauses

    for query in query_frequency:
        parsed_query = sql_metadata.Parser(query)

        if not WHERE_CLAUSE in parsed_query.columns_dict:
            continue
        for column in parsed_query.columns_dict[WHERE_CLAUSE]:
            qfied_column = ddl.get_qualified_column(parsed_query.tables, column)

            column_access_frequency[qfied_column] = (
                column_access_frequency.get(qfied_column, 0) + query_frequency[query]
            )

    for key, value in column_access_frequency.items():
        logger.info(f"Freq: {value}, column: {key}")


def parse_ddl_file(ddl_file):
    """
    Returns:
        DDL: A representation of the DDL defined in the file.
    """
    # TODO: Handle errors
    return DDL.from_file(ddl_file)


def parse_sql_log(log_file):
    query_frequency = {}

    with open(log_file) as f_ptr:
        # TODO: Identify quotes and delimiters
        reader = csv.reader(f_ptr, delimiter=",")
        for row in reader:
            if len(row) != len(CSV_LOG_KEYS):
                logger.error("Failed to parse row: %s" % row_as_str(row))
                break

            row_dict = {CSV_LOG_KEYS[i]: row[i] for i in range(len(CSV_LOG_KEYS))}

            # Ignore transaction begin and end markers
            if row_dict["command_tag"] in EXCLUDE_COLLECTION:
                continue

            # Strip off the execution context
            exec_index = row_dict["message"].find(
                ": ",
            )

            query = row_dict["message"][exec_index + 1 :]
            query = query.strip()

            # After cleaning, check if query is one of COMMIT/BEGIN
            # This can happen when the log doesn't record the command tag correctly
            if query.strip() in EXCLUDE_COLLECTION:
                continue

            query_frequency[query] = query_frequency.get(query, 0) + 1

            # logger.info(row_dict["message"][exec_index + 1 :])
            # # Parse the node
            # root = pglast.Node(pglast.parse_sql(row_dict["message"][exec_index + 1 :]))
            # for node in root.traverse():
            #     print(node)

            # count += 1
            # if count > max_rows:
            #     break

    for key, value in query_frequency.items():
        query = sqlparse.format(key, strip_whitespace=True)
        # if query != key:
        #     query_frequency[query] = key
        #     del query_frequency[key]

        logger.info(f"Freq: {value}, query: {query}")

    return query_frequency


def main():
    parser = argparse.ArgumentParser("Databases Runner")
    parser.add_argument(
        "--log_file", type=str, dest="log_file", help="Log file to be parsed"
    )

    parser.add_argument(
        "--ddl_file",
        type=str,
        dest="ddl_file",
        help="DDL file for the workload",
        default="/home/kramana2/benchbase/src/main/resources/benchmarks/epinions/ddl-postgres.sql",
    )

    args = parser.parse_args()

    logger.debug("Obtained log file: %s" % (args.log_file))
    ddl = parse_ddl_file(args.ddl_file)
    queries = parse_sql_log(args.log_file)
    process_queries(ddl, queries)

    db = Postgres()
    db.connect()
    db.disconnect()


if __name__ == "__main__":
    main()
