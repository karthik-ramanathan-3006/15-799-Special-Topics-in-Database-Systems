from pathlib import Path


WHERE_CLAUSE = "where"

# DATABASE Connection constants
DB_USERNAME = "project1user"
DB_PASSWORD = "project1pass"
DEFAULT_DB = "project1db"

VERBOSITY_DEFAULT = 2

MACHINE = "lab-machine"

DATA_STORE = "data.json"

# Benchmark constants
EPINIONS = "epinions"
INDEXJUNGLE = "indexjungle"
TIMESERIES = "timeseries"

BENCHMARKS = [
    EPINIONS,
    INDEXJUNGLE,
    TIMESERIES,
]

# File Paths
TLD = Path(__file__).parent
DDL_DIRECTORY = TLD / "ddls/"
RESULTS_PATH = TLD / "results.txt"

KEY_TABLE_INDEXES = "table_indexes"
KEY_INDEX_COLUMNS = "column_indexes"
