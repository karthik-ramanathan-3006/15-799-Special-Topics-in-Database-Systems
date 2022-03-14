import itertools
import logging
from math import floor
from typing import Dict, List
import numpy as np
from scipy.stats import qmc

from constants import (
    BENCHMARKS,
    EPINIONS,
    INDEXJUNGLE,
    KEY_INDEX_COLUMNS,
    KEY_TABLE_INDEXES,
    SCRIPTS_DIRECTORY,
    TIMESERIES,
)
from ddl import DDL
from results import BenchbaseRun, Index
from util import construct_index_args, construct_index_name, get_ddl_for_benchmark

logging.basicConfig()
logger = logging.getLogger("sampler")
logger.setLevel(logging.DEBUG)


# 4. Choice of benchmark: 1, 2, 3
# 5. Indexes, choice:

# Let's define the dimension spaces
TIME_SPACE = np.linspace(start=60, stop=300, num=9)
RATE_SPACE = np.logspace(start=1, stop=4)  # ie. 10 to 10,000
SCALEFACTOR_SPACE = np.logspace(start=-2, stop=3, num=6)  # ie. 0.01 to 1000


MAX_COLS_PER_INDEX = 3
MAX_INDEXES_PER_DATABASE = 5


def parse_ddl():
    ddl_map = {}
    for benchmark in BENCHMARKS:
        ddl = get_ddl_for_benchmark(benchmark)

        # For each table enumerate all possible indexes.
        ddl_map[benchmark] = {KEY_INDEX_COLUMNS: {}, KEY_TABLE_INDEXES: []}
        for table in ddl.tables:
            logger.info(f"Generating combinations for {table}")
            combs = []

            # Exhaustively enumerate all possible index-column combinations
            combs.extend(itertools.combinations(ddl.tables[table].columns, 3))
            combs.extend(itertools.combinations(ddl.tables[table].columns, 2))
            combs.extend(itertools.combinations(ddl.tables[table].columns, 1))
            # logger.info(f"Generated combinations for {table}: {combs}")

            ddl_map[benchmark][KEY_INDEX_COLUMNS][table] = combs

        table_combinations = []
        for i in range(1, MAX_INDEXES_PER_DATABASE + 1):
            table_combinations.extend(itertools.combinations(ddl.tables.keys(), i))

        ddl_map[benchmark][KEY_TABLE_INDEXES] = table_combinations[:]
        logger.info(
            f"Generated combinations for benchmark {benchmark}: {table_combinations}"
        )

    return ddl_map


# In order to avoid biasing tables with a large number of columns, we pick the table first, following which we randomly pick columns.


def generate_samples(ddl_map: Dict):
    # We generate samples on a per benchmark basis
    # Factors:
    # 1. Amount of time run: 60s to 600s, linear
    # 2. Rate: 10 to 10,000, log
    # 3. Scale factor: 0.01 to 1000, log
    # 4. Choice and number of indexes.

    # For epinions
    # The upper and lower bounds for the sampler
    NUM_SAMPLES = 50
    epinions_data = ddl_map[EPINIONS]
    l_bounds = np.array([0, 0, 0, 0])
    u_bounds = np.array([9, 50, 5, len(epinions_data[KEY_TABLE_INDEXES])])

    NUM_DIMENSIONS = len(l_bounds)
    epinions_sampler = qmc.LatinHypercube(d=NUM_DIMENSIONS)

    # space = np.array([TIME_SPACE, RATE_SPACE, SCALEFACTOR_SPACE, benchmark_space], dtype=object)

    samples = epinions_sampler.random(n=NUM_SAMPLES)
    scaled_samples = qmc.scale(samples, l_bounds, u_bounds)

    epinions_samples: List[BenchbaseRun] = []
    for sample in scaled_samples:
        sample_indexes = [int(floor(val)) for val in sample]
        # sample_in_space = [s[i][sample_indexes] for i, s in enumerate(space)]
        logger.info(f"Epinions sample: {sample_indexes}")

        workload_indexes: List[Index] = []
        for table in epinions_data[KEY_TABLE_INDEXES][sample_indexes[3]]:
            columns = np.random.choice(epinions_data[KEY_INDEX_COLUMNS][table])
            index_name = construct_index_name(table, list(columns))
            workload_indexes.append(Index(index_name, table, list(columns)))

        e_sample = {
            "time": int(TIME_SPACE[sample_indexes[0]]),
            "rate": int(RATE_SPACE[sample_indexes[1]]),
            "scalefactor": round(SCALEFACTOR_SPACE[sample_indexes[2]], ndigits=3),
            "indexes": workload_indexes,
        }

        bb_run = BenchbaseRun(
            EPINIONS,
            workload_indexes,
            log_directory=None,
            scalefactor=round(SCALEFACTOR_SPACE[sample_indexes[2]], ndigits=3),
            time=int(TIME_SPACE[sample_indexes[0]]),
            rate=int(RATE_SPACE[sample_indexes[1]]),
        )

        epinions_samples.append(bb_run)
        logger.info(f"Epinions sample: {e_sample}")

    return epinions_samples


def get_samples(sampler, num_samples, lower_bounds, upper_bounds, ddl_data, benchmark):
    samples = sampler.random(n=num_samples)
    scaled_samples = qmc.scale(samples, lower_bounds, upper_bounds)

    benchmark_samples: List[BenchbaseRun] = []
    for sample in scaled_samples:
        sample_indexes = [int(floor(val)) for val in sample]

        workload_indexes: List[Index] = []
        if len(ddl_data[KEY_TABLE_INDEXES]) == 1:
            table = ddl_data[KEY_TABLE_INDEXES][0][0]

            columns = ddl_data[KEY_INDEX_COLUMNS][table][sample_indexes[3]]
            index_name = construct_index_name(table, list(columns))
            workload_indexes.append(Index(index_name, table, list(columns)))
        else:
            # There is more than one table.
            for table in ddl_data[KEY_TABLE_INDEXES][sample_indexes[3]]:
                columns = np.random.choice(ddl_data[KEY_INDEX_COLUMNS][table])
                index_name = construct_index_name(table, list(columns))
                workload_indexes.append(Index(index_name, table, list(columns)))

        e_sample = {
            "time": int(TIME_SPACE[sample_indexes[0]]),
            "rate": int(RATE_SPACE[sample_indexes[1]]),
            "scalefactor": round(SCALEFACTOR_SPACE[sample_indexes[2]], ndigits=3),
            "indexes": workload_indexes,
        }

        bb_run = BenchbaseRun(
            benchmark,
            workload_indexes,
            log_directory=None,
            scalefactor=round(SCALEFACTOR_SPACE[sample_indexes[2]], ndigits=3),
            time=int(TIME_SPACE[sample_indexes[0]]),
            rate=int(RATE_SPACE[sample_indexes[1]]),
        )

        benchmark_samples.append(bb_run)
        logger.info(f"Samples: {e_sample}")

    return benchmark_samples


def generate_indexjungle_samples(ddl_map: Dict):
    NUM_SAMPLES = 50
    ij_data = ddl_map[INDEXJUNGLE]

    # Indexjungle has a single table, and so doesn't need the 4th dimension
    table_name = ij_data[KEY_TABLE_INDEXES][0][0]
    l_bounds = np.array([0, 0, 0, 0])
    u_bounds = np.array([9, 50, 5, len(ij_data[KEY_INDEX_COLUMNS][table_name])])

    NUM_DIMENSIONS = len(l_bounds)
    assert len(ij_data[KEY_TABLE_INDEXES]) == 1, "More than 1 table found in IJ"

    ij_sampler = qmc.LatinHypercube(d=NUM_DIMENSIONS)
    return get_samples(
        ij_sampler, NUM_SAMPLES, l_bounds, u_bounds, ij_data, INDEXJUNGLE
    )


def generate_timeseries_samples(ddl_map: Dict):
    NUM_SAMPLES = 50
    ts_data = ddl_map[TIMESERIES]

    l_bounds = np.array([0, 0, 0, 0])
    u_bounds = np.array([9, 50, 5, len(ts_data[KEY_TABLE_INDEXES])])

    NUM_DIMENSIONS = len(l_bounds)
    ts_sampler = qmc.LatinHypercube(d=NUM_DIMENSIONS)
    return get_samples(ts_sampler, NUM_SAMPLES, l_bounds, u_bounds, ts_data, TIMESERIES)


def get_column_args(columns) -> str:
    if len(columns) == 0:
        logger.warn("Number of columns is 0!")
        return ""

    return " -c ".join(columns)


def scriptify_samples(samples: List[BenchbaseRun], script_file="script.sh"):
    benchmark = samples[0].benchmark
    script_file = SCRIPTS_DIRECTORY / f"{benchmark}_{script_file}"

    lines = ["#!/bin/bash", "source ~/project/bin/activate;"]
    for i, sample in enumerate(samples):
        # Let's assume that the DB contains no indexes.
        # First, create each index.
        lines.append(f"# Beginning of sampling {i+1}")

        for index in sample.indexes:
            lines.append(
                f"doit create_index --table {index.table} -c {get_column_args(index.columns)};"
            )

        index_args = construct_index_args(sample.indexes)
        lines.append(
            f"doit run_workload --benchmark {sample.benchmark} --scalefactor {sample.scalefactor} --time {sample.time} --rate {sample.rate} -i {index_args}"
        )

        # Finally, drop each of the indexes.
        for index in sample.indexes:
            lines.append(
                f"doit drop_index --table {index.table} -c {get_column_args(index.columns)};"
            )

        lines.append("")
        lines.append(f"# End of sampling {i+1}")
        lines.append("")
        lines.append("")

    script = "\n".join(lines)

    with open(script_file, "w") as fp:
        fp.write(script)


ddl_map = parse_ddl()
samples = generate_timeseries_samples(ddl_map)
scriptify_samples(samples)
