from pathlib import Path
import logging
import uuid
from constants import VERBOSITY_DEFAULT, DEFAULT_DB, DB_USERNAME, DB_PASSWORD
from dodos.dodo import POSTGRES_PATH, POSTGRES_DATA_PATH
from doit.action import CmdAction
from plumbum import local

from results import BenchbaseRun, parse_results
from util import construct_index_name, get_index_from_name

logging.basicConfig()
logger = logging.getLogger("dodo")
logger.setLevel(logging.DEBUG)

BASE_DODOS_DIRECTORY = "dodos/"
PSQL = "/home/kramana2/postgres/build/bin/psql"


run_directory = None


def task_run_workload():
    global run_directory
    run_directory = Path(POSTGRES_DATA_PATH) / str(uuid.uuid4())
    results_directory = run_directory / "results"
    logger.info(f"Storing results in directory: {run_directory}")

    def get_column_args(columns) -> str:
        if len(columns) == 0:
            logger.warn("Number of columns is 0!")
            return ""

        return " -c ".join(columns)

    def invoke_create_index(table, columns):
        return f"cd {BASE_DODOS_DIRECTORY}; doit create_index --table {table} -c {get_column_args(columns)}"

    def invoke_drop_index(table, columns):
        return f"cd {BASE_DODOS_DIRECTORY}; doit drop_index --table {table} -c {get_column_args(columns)}"

    def invoke_store_results(benchmark, scalefactor, time, rate, indexes):
        global run_directory
        index_list = []
        for index in indexes:
            index_list.append(get_index_from_name(benchmark, index))

        run = BenchbaseRun(
            benchmark=benchmark,
            indexes=index_list,
            log_directory=run_directory,
            scalefactor=scalefactor,
            time=time,
            rate=rate,
        )

        parse_results(run)
        return "echo 'Run successful!'"

    return {
        "actions": [
            f"mkdir -p {results_directory}",
            f"cd {BASE_DODOS_DIRECTORY}; doit update_config --benchmark=%(benchmark)s --scalefactor=%(scalefactor)f --time=%(time)d --rate=%(rate)d --terminals=%(terminals)d",
            f'cd {BASE_DODOS_DIRECTORY}; doit update_log_collection --log_directory="{run_directory}"',
            # Hack to restart Postgres
            lambda: local[f"{POSTGRES_PATH}/pg_ctl"][
                "-D", POSTGRES_DATA_PATH, "restart"
            ].run_fg(),
            f"until {POSTGRES_PATH}/pg_isready ; do sleep 1 ; done",
            # Initialize the benchmark
            # f'cd {BASE_DODOS_DIRECTORY}; doit benchbase_workload_create --benchmark="%(benchmark)s" --directory="{results_directory}"',
            f"cd {BASE_DODOS_DIRECTORY}; doit perform_vacuum;"
            f'cd {BASE_DODOS_DIRECTORY}; doit benchbase_run --benchmark="%(benchmark)s" --args="--execute=true" --directory="{results_directory}"',
            CmdAction(
                invoke_store_results,
            ),
        ],
        "params": [
            {
                "name": "benchmark",
                "long": "benchmark",
                "help": "The benchmark to run.",
                "default": "epinions",
            },
            {
                "name": "scalefactor",
                "long": "scalefactor",
                "type": float,
                "default": 1.0,
            },
            {
                "name": "time",
                "long": "time",
                "type": int,
                "default": 60,  # 60s
            },
            {
                "name": "rate",
                "long": "rate",
                "type": int,
                "default": 10,
            },
            {
                "name": "terminals",
                "long": "terminals",
                "default": 1,
            },
            {
                "name": "indexes",
                "long": "indexes",
                "short": "i",
                "type": list,
                "default": [],
            },
        ],
        "verbosity": VERBOSITY_DEFAULT,
    }


def task_create_index():
    """
    Creates a single index on the given table.
    """

    def invoke_create_index(table, columns):
        column_list_str = ", ".join(columns)
        index_name: str = construct_index_name(table, columns)

        sql = f"CREATE INDEX IF NOT EXISTS {index_name} ON {table} ({column_list_str});"
        return f'PGPASSWORD={DB_PASSWORD} {PSQL} --host=localhost --dbname={DEFAULT_DB} --username={DB_USERNAME} --command="{sql}"'

    return {
        "actions": [
            CmdAction(invoke_create_index),
        ],
        "params": [
            {
                "name": "table",
                "long": "table",
                "default": "",
            },
            {
                "name": "columns",
                "long": "columns",
                "short": "c",
                "type": list,
                "default": [],
            },
        ],
        "verbosity": VERBOSITY_DEFAULT,
    }


def task_drop_index():
    """
    Deletes a single index on the given table.
    """

    def invoke_drop_index(table, columns):
        index_name: str = construct_index_name(table, columns)

        sql = f"DROP INDEX IF EXISTS {index_name};"
        return f'PGPASSWORD={DB_PASSWORD} {PSQL} --host=localhost --dbname={DEFAULT_DB} --username={DB_USERNAME} --command="{sql}"'

    return {
        "actions": [
            CmdAction(invoke_drop_index),
        ],
        "params": [
            {
                "name": "table",
                "long": "table",
                "default": "",
            },
            {
                "name": "columns",
                "long": "columns",
                "short": "c",
                "type": list,
                "default": [],
            },
        ],
        "verbosity": VERBOSITY_DEFAULT,
    }
