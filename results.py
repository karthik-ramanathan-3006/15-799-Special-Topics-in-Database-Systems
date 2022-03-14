from glob import glob
import json
import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from pprint import pprint
from typing import List
from constants import MACHINE, RESULTS_DIRECTORY
from ddl import Index

logging.basicConfig()
logger = logging.getLogger("results")
logger.setLevel(logging.DEBUG)


@dataclass
class BenchbaseRun:
    benchmark: str = None
    indexes: List[Index] = field(default_factory=list)
    log_directory: str = None
    scalefactor: float = 1.0
    time: int = 60
    rate: int = 10
    terminals: int = 1


def writeout_results(data, data_file="results.json"):
    benchmark = data["benchmark"]
    script_file = RESULTS_DIRECTORY / f"{benchmark}_{data_file}"

    with open(script_file, "a") as results_file:
        json.dump(data, results_file)
        results_file.write("\n")


def parse_results(run: BenchbaseRun) -> dict:
    directory_path = Path(run.log_directory)
    results_path = directory_path / "results"

    # Indirectly check that both paths exist.
    if not results_path.exists():
        logger.error(f"Path {run.log_directory} does not exist")
        return

    regex = str(results_path) + "/*.summary.json"
    files = glob(regex)
    assert len(files) == 1, f"Found {len(files)} matching files; expected 1"

    summary_file_path = files[0]
    regex = f"{run.benchmark}\_(.+?)\.summary\.json"
    matches = re.search(regex, summary_file_path)
    assert matches, "Could not understand file format"
    timestamp = matches.group(1)

    # Parse the results
    results = {}
    with open(summary_file_path, "r") as results_json:
        results = json.load(results_json)

    data = {
        # Benchbase details
        "benchmark": run.benchmark,
        "scalefactor": run.scalefactor,
        "rate": run.rate,
        "time": run.time,
        "terminals": run.terminals,
        # Indexes
        "indexes": [
            {
                "name": index.name,
                "table": index.table,
                "columns": index.columns,
            }
            for index in run.indexes
        ],
        # Results: TBD
        "data": results,
        # Reverse engineering details
        "timestamp": timestamp,
        "log_directory": str(run.log_directory),
        "results": summary_file_path,
        "machine": MACHINE,
    }

    data["timestamp"] = timestamp
    pprint(data)
    writeout_results(data)


# def main():
#     run = BenchbaseRun("timeseries", [Index("sources_created_time", "sources", ["created_time"])], "/home/kramana2/postgresql/data/37a261eb-942f-4dea-b04c-4dd26284e5aa")
#     parse_results(run)
