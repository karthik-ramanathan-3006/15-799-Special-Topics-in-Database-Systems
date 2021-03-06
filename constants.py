from pathlib import Path


WHERE_CLAUSE = "where"

# DATABASE Connection constants
DB_USERNAME = "project1user"
DB_PASSWORD = "project1pass"
DEFAULT_DB = "project1db"

VERBOSITY_DEFAULT = 2

MACHINE = "lab-machine"

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
RESULTS_DIRECTORY = TLD / "benchbase_data/"
SCRIPTS_DIRECTORY = TLD / "scripts/"
TEMP_CSV = TLD / "temp.csv"
ACTIONS_SQL = TLD / "actions.sql"
STATE_DIRECTORY = TLD / "state/"
STATE_JSON = STATE_DIRECTORY / "state.json"
STATE_CANDIDATES = STATE_DIRECTORY / "candidates.txt"


KEY_TABLE_INDEXES = "table_indexes"
KEY_INDEX_COLUMNS = "column_indexes"
