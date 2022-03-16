from typing import List
from constants import DDL_DIRECTORY, EPINIONS, TEMP_CSV
from ddl import DDL, Index
import logging


logging.basicConfig()
logger = logging.getLogger("util")
logger.setLevel(logging.DEBUG)


def get_logger(name: str):
    """
    Fetches a logger with the requested configuration
    """
    logging.basicConfig()
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    return logger


def get_ddl_for_benchmark(benchmark: str) -> DDL:
    """
    Fetches the DDL for the given benchmark.
    """
    ddl_file = DDL_DIRECTORY / f"{benchmark}.sql"
    return DDL.from_file(ddl_file)


def construct_index_args(indexes: Index) -> str:
    if len(indexes) == 0:
        logger.warn("Number of indexes is 0!")
        return ""

    return " -i ".join([index.name for index in indexes])


def construct_index_name(table: str, columns: List[str]) -> str:
    """
    Constructs the name of an index.
    """
    return f"{table}_" + "_".join(columns)


def get_index_from_name(benchmark: str, index_name: str) -> Index:
    """
    Decomposes the name of an index into its constituent parts.
    """
    ddl = get_ddl_for_benchmark(benchmark)
    parts = index_name.split("_")
    i = 0

    # First, figure out the table name
    table_name = parts[i]
    while True:
        if table_name in ddl.tables.keys():

            # Hack, sust for epinions, do the following check
            temp_table_name = table_name + "_" + parts[i + 1]
            if temp_table_name in ddl.tables.keys():
                table_name += "_" + parts[i + 1]
                i += 1
                continue

            i += 1
            break

        table_name += "_" + parts[i + 1]
        i += 1

    logger.debug(f"Table name: {table_name}")

    table = ddl.tables[table_name]
    columns = []
    column_name = parts[i]
    while i != len(parts):
        if column_name in table.columns:
            columns.append(column_name)
            logger.debug(f"Found column: {column_name}")

            if (i + 1) != len(parts):
                column_name = parts[i + 1]
            i += 1
            continue

        if (i + 1) != len(parts):
            column_name += "_" + parts[i + 1]
        i += 1

    return Index(index_name, table_name, columns)


def row_as_str(row_array: List) -> str:
    """
    Converts the given row array into a string.
    """
    return ", ".join(row_array)


def print_indexes(index_list: List[Index]) -> str:
    """
    A handy function to stringify the given index.
    """
    return str([index.name for index in index_list])

def combine_csvs(files: str):
    with open(TEMP_CSV, "w") as out_file:
        for file in files:
            with open(str(file), "r") as in_file:
                out_file.write(in_file.read())

