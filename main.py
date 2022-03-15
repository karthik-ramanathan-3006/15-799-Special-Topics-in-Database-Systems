import argparse
import logging
import pglast


from ddl import DDL
from parse_log import parse_sql_log, process_queries
from postgres import Postgres

logging.basicConfig()
logger = logging.getLogger("15-799")
logger.setLevel(logging.DEBUG)


def parse_ddl_file(ddl_file):
    """
    Returns:
        DDL: A representation of the DDL defined in the file.
    """
    # TODO: Handle errors
    return DDL.from_file(ddl_file)


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
