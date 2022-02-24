import argparse
import csv
import logging
import pglast

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


def parse_sql_log(log_file):

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

            logger.info(row_dict["message"][exec_index + 1 :])
            # Parse the node
            root = pglast.Node(pglast.parse_sql(row_dict["message"][exec_index + 1 :]))
            for node in root.traverse():
                print(node)

            break


def main():
    parser = argparse.ArgumentParser("Databases Runner")
    parser.add_argument(
        "--log_file", type=str, dest="log_file", help="Log file to be parsed"
    )

    args = parser.parse_args()

    logger.debug("Obtained log file: %s" % (args.log_file))
    parse_sql_log(args.log_file)


if __name__ == "__main__":
    main()
