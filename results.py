from glob import glob
import json
import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from pprint import pprint
from typing import List
from constants import BENCHMARKS, EPINIONS, INDEXJUNGLE, MACHINE, RESULTS_DIRECTORY, TIMESERIES
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


GPR_THRESHOLD = 0.65

def parse_run_data(benchmark, directory=RESULTS_DIRECTORY) -> List[List[Index]]:
    """
    Parse the results of the runs on the NUC.
    Returns a set of candidate indexes.
    """
    
    file = RESULTS_DIRECTORY / f"{benchmark}_results.json"

    
    results = []
    # Process it line by line.
    with open(file, "r") as fp:
        raw_line_data = None
        for raw_line_data in fp:
            line_data = json.loads(raw_line_data)
            goodput = round(float(line_data["data"]["Goodput (requests/second)"]), 2)
            rate = int(line_data["rate"])
            indexes = line_data["indexes"]
            
            gp_per_rate = round((goodput / rate), 2)
            
            
            results.append((goodput, rate, indexes, gp_per_rate))
            # We've printed duplicated data. So advance the pointer
            # by a line
            fp.readline()
    
    results.sort(key=lambda x: x[-1], reverse=True)

    # Filter out the best results; the number don't matter so much
    best_results = []
    for result in results:
        if result[-1] < GPR_THRESHOLD:
            break
            
        best_results.append(result)
        
        indexes = result[2]
        index_names = [index["name"] for index in indexes]
        logger.info(f"Goodput: {result[0]} \t Rate: {result[1]} \t Avg: {result[3]} \t Indexes: {index_names}")

    # Return the candidate indexes
    return [result[2] for result in best_results]

