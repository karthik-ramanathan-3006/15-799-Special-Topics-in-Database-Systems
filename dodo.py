import logging
import os
from plumbum import cmd, local
from pathlib import Path

import doit
from doit.action import CmdAction

from xml.etree import ElementTree

from constants import DEFAULT_DB, DB_USERNAME, DB_PASSWORD

logging.basicConfig()
logger = logging.getLogger("dodo")
logger.setLevel(logging.DEBUG)

NOISEPAGE_PATH = Path.joinpath(Path.home(), "noisepage-pilot").absolute()
ARTIFACTS_PATH = Path.joinpath(NOISEPAGE_PATH, "artifacts/benchbase")
PROJECT_PATH = Path.joinpath(NOISEPAGE_PATH, "artifacts/project")
POSTGRES_PATH = str(Path.joinpath(Path.home(), "postgres/build/bin"))
POSTGRES_DATA_PATH = str(Path.joinpath(Path.home(), "postgresql/data"))
ARTIFACT_benchbase = Path.joinpath(ARTIFACTS_PATH, "benchbase.jar")

PSQL = "/home/kramana2/postgres/build/bin/psql"

BENCHBASE_CONFIG_TAGS = {
    "scalefactor": "/parameters/scalefactor",
    "time": "/parameters/works/work/time",
    "rate": "/parameters/works/work/rate",
    "terminals": "/parameters/terminals",
}

VERBOSITY_DEFAULT = 2


def task_hello():
    return {"actions": ["echo 'Hello world!'"], "verbosity": VERBOSITY_DEFAULT}


def get_config_path(benchmark, config=None) -> str:
    """
    Fetches the path to the config file of the given benchmark.
    """
    if config is None:
        config = PROJECT_PATH / f"{benchmark}_config.xml"
    elif not config.startswith("/"):
        config = Path(NOISEPAGE_PATH / config).absolute()

    return str(config)


def task_update_log_collection():
    sql_list = [
        "ALTER SYSTEM SET log_destination='csvlog'",
        "ALTER SYSTEM SET logging_collector='on'",
        "ALTER SYSTEM SET log_statement='all'",
        "ALTER SYSTEM SET log_connections='on'",
        "ALTER SYSTEM SET log_disconnections='on'",
        "ALTER SYSTEM SET log_directory='%(log_directory)s'",
    ]

    return {
        "actions": [
            f"mkdir -p {POSTGRES_DATA_PATH}/%(log_directory)s",
            *[
                f'PGPASSWORD={DB_PASSWORD} {PSQL} --host=localhost --dbname={DEFAULT_DB} --username={DB_USERNAME} --command="{sql}"'
                for sql in sql_list
            ],
            lambda: local[f"{POSTGRES_PATH}/pg_ctl"][
                "-D", POSTGRES_DATA_PATH, "restart"
            ].run_fg(),
            f"until {POSTGRES_PATH}/pg_isready ; do sleep 1 ; done",
        ],
        "params": [
            {
                "name": "log_directory",
                "long": "log_directory",
                "default": "log",
            },
            {
                "name": "log_file",
                "long": "log_file",
                "default": "postgresql-%Y-%m-%d_%H%M%S.log",
            },
        ],
        "verbosity": VERBOSITY_DEFAULT,
    }


def task_update_config():
    def update_xml(benchmark, scalefactor=1, time=60, rate=10, terminals=1):
        kwargs = locals().copy()
        del kwargs["benchmark"]

        config = get_config_path(benchmark)
        logger.info(f"Updating arguments in config file {config} with values: {kwargs}")

        actions = []
        for param in kwargs:
            # We're assuming that all keys in kwargs are in BENCHBASE_CONFIG_TAGS
            key = BENCHBASE_CONFIG_TAGS[param]
            value = locals()[param]
            cmd = f"xmlstarlet edit --inplace --update '{key}' --value \"{value}\" {config}"
            actions.append(cmd)

        return "; \n".join(actions)

    return {
        "actions": [
            CmdAction(update_xml),
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
        ],
        "verbosity": VERBOSITY_DEFAULT,
    }


def task_benchbase_run():
    """
    BenchBase: run a specific benchmark.
    """

    def invoke_benchbase(benchmark, config, args):
        config = get_config_path(benchmark, config)
        return (
            f"echo {config}; java -jar benchbase.jar -b {benchmark} -c {config} {args}"
        )

    return {
        "actions": [
            lambda: os.chdir(str(ARTIFACTS_PATH)),
            # Invoke BenchBase.
            CmdAction(invoke_benchbase),
            # Reset working directory.
            lambda: os.chdir(doit.get_initial_workdir()),
        ],
        "file_dep": [ARTIFACT_benchbase],
        "uptodate": [False],
        "verbosity": VERBOSITY_DEFAULT,
        "params": [
            {
                "name": "benchmark",
                "long": "benchmark",
                "help": "The benchmark to run.",
                "default": "epinions",
            },
            {
                "name": "config",
                "long": "config",
                "help": (
                    "The config file to use for BenchBase."
                    "Defaults to the config in the artifacts folder for the selected benchmark."
                ),
                "default": None,
            },
            {
                "name": "args",
                "long": "args",
                "help": "Arguments to pass to BenchBase invocation.",
                "default": "--create=false --load=false --execute=false",
            },
        ],
    }
