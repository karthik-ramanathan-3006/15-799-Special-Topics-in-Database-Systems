"""
Houses all the query parsing logic
"""

import csv
from typing import Mapping, Tuple
import sql_metadata
import sqlparse

from constants import WHERE_CLAUSE
from ddl import DDL
from util import get_logger, row_as_str

logger = get_logger("parser")

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

# The only query types that we care about
ALLOWED_QUERY_TYPES = ["INSERT", "UPDATE", "SELECT", "DELETE"]


def parse_sql_log(log_file: str):
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

            if not query.split():
                continue

            if query.split()[0] not in ALLOWED_QUERY_TYPES:
                continue

            # Ignore the query if it is a Postgres catalog query
            if "pg_stat" in query or "pg_catalog" in query:
                continue

            query_frequency[query] = query_frequency.get(query, 0) + 1

    for key, value in query_frequency.items():
        query = sqlparse.format(key, strip_whitespace=True)
        # logger.info(f"Freq: {value}, query: {query}")

    return query_frequency


def process_queries(ddl: DDL, query_frequency):
    """ """
    table_access_frequency = {}
    column_access_frequency = {}
    # Mpas a tuple of columns to the
    query_template_frequency: Mapping[Tuple[str], int] = {}
    column_importance_frequency = {}

    # Things to account for:
    # 1. Query type: SELECT vs UPDATE vs INSERT
    # 2. WHERE CLAUSE and order of columns
    # 3. Subqueries:
    # 4. LIMIT and offset
    # 5. JOIN clauses (a.colA v b.colA)
    # 6. Clean out values from WHERE clauses

    for query in query_frequency:
        parsed_query = sql_metadata.Parser(query)

        try:
            if not parsed_query or not parsed_query.columns_dict:
                continue
        except IndexError:
            # SQL Metadata Parser errors out on rare occasions.
            continue

        if not WHERE_CLAUSE in parsed_query.columns_dict:
            continue

        columns_accessed = []
        for column in parsed_query.columns_dict[WHERE_CLAUSE]:

            qfied_column = ddl.get_qualified_column(parsed_query.tables, column)

            if not qfied_column:
                # This means that the column is not a part of the given DDL.
                # Silently error out and move on.
                continue

            column_access_frequency[qfied_column] = (
                column_access_frequency.get(qfied_column, 0) + query_frequency[query]
            )

            columns_accessed.append(qfied_column)

        if columns_accessed:
            columns_accessed = tuple(columns_accessed)
            query_template_frequency[columns_accessed] = (
                query_template_frequency.get(columns_accessed, 0)
                + query_frequency[query]
            )

    # Print a summary, if column access frequency has been populated.
    if column_access_frequency:
        for key, value in column_access_frequency.items():
            logger.info(f"Freq: {value}, column: {key}")

    if query_template_frequency:
        for key, value in query_template_frequency.items():
            logger.info(f"Freq: {value}, ordered columns: {key}")
            for (i, column) in enumerate(key):
                # Let's assume that the importance of columns
                # follows exponential backoff
                # This might not be true for OR clauses, but let's pretend that it is.
                const = 1 / (2**i)
                column_importance_frequency[column] = column_importance_frequency.get(
                    column, 0
                ) + round((const * value), 2)

        for key, value in column_importance_frequency.items():
            logger.info(f"Freq: {value}, column: {key}")

    return {
        "column_access": column_access_frequency,
        "column_importance": column_importance_frequency,
        "query_templates": query_template_frequency,
    }
