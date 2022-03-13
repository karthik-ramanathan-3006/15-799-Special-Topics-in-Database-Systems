from pathlib import Path
import logging
import uuid
from constants import VERBOSITY_DEFAULT
from dodos.dodo import POSTGRES_PATH, POSTGRES_DATA_PATH
from doit.action import CmdAction
from plumbum import local

logging.basicConfig()
logger = logging.getLogger("dodo")
logger.setLevel(logging.DEBUG)

BASE_DODOS_DIRECTORY = "dodos/"


def task_run_workload():
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

    return {
        "actions": [
            f"mkdir -p {results_directory}",
            f"cd {BASE_DODOS_DIRECTORY}; doit update_config --scalefactor=%(scalefactor)d --time=%(time)d --rate=%(rate)d --terminals=%(terminals)d",
            f'cd {BASE_DODOS_DIRECTORY}; doit update_log_collection --log_directory="{run_directory}"',
            # Hack to restart Postgres
            lambda: local[f"{POSTGRES_PATH}/pg_ctl"][
                "-D", POSTGRES_DATA_PATH, "restart"
            ].run_fg(),
            f"until {POSTGRES_PATH}/pg_isready ; do sleep 1 ; done",
            CmdAction(invoke_create_index),
            f'cd {BASE_DODOS_DIRECTORY}; doit benchbase_run --benchmark="%(benchmark)s" --args="--execute=true" --directory="{results_directory}"',
            CmdAction(invoke_drop_index),
            # Hack to restart Postgres
            lambda: local[f"{POSTGRES_PATH}/pg_ctl"][
                "-D", POSTGRES_DATA_PATH, "restart"
            ].run_fg(),
            f"until {POSTGRES_PATH}/pg_isready ; do sleep 1 ; done",
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
                "default": 1,
            },
            {
                "name": "time",
                "long": "time",
                "default": 60,  # 60s
            },
            {
                "name": "rate",
                "long": "rate",
                "default": 10,
            },
            {
                "name": "terminals",
                "long": "terminals",
                "default": 1,
            },
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
