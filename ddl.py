from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Mapping

import logging
import sql_metadata
import sqlparse

logging.basicConfig()
logger = logging.getLogger("DDL")
logger.setLevel(logging.DEBUG)


class IndexType:
    BTREE: str = "btree"
    BRIN: str = "brin"
    HASH: str = "hash"


@dataclass
class Index:
    name: str = None
    table: str = None
    columns: List[str] = field(default_factory=list)
    itype: IndexType = IndexType.BTREE


@dataclass
class Table:
    name: str = None
    columns: List[str] = field(default_factory=list)


@dataclass
class DDL:
    tables: Mapping[str, Table]
    name: str = None

    @staticmethod
    def from_sql_statements(statements: List[str]):
        tables: Mapping[str, Table] = {}

        for stmt in statements:
            parsed_stmt = sql_metadata.Parser(stmt)
            table_name = None
            try:

                if parsed_stmt.query_type == sql_metadata.QueryType.CREATE:
                    # Since we're creating a table, there's got to be only 1 table.
                    table_name = parsed_stmt.tables[0]
                    tables[table_name] = Table(table_name, parsed_stmt.columns)
                    logger.info(f"Successfully processed DDL for table {table_name}.")
                    continue

                # We know that DROP TABLE doesn't get processed.
                # What else might we encounter?

                logger.info(f"Encountered statement: {parsed_stmt.query_type}")

            except ValueError:
                logger.error(f"Cannot process query: {stmt}")

            # No worries, just proceed forward

        return DDL(tables)

    @staticmethod
    def from_file(filename: Path):
        # 1. Read the file into memory
        with open(filename, "r") as file:
            text = file.read()

        # 2. Strip out the comments
        text = sqlparse.format(text, strip_comments=True)

        # 3. Split text into SQL statements
        statements = sqlparse.split(text)

        ddl = DDL.from_sql_statements(statements)
        # Quick hack to name the DDL
        benchmark = str(filename)[: -len(".sql")]
        ddl.name = benchmark
        return ddl

    def has_table(self, table: str) -> bool:
        return table in self.tables.keys()

    def get_qualified_column(self, possible_tables: List[str], column: str) -> str:
        # The column may already be qualified.
        parts = column.split(".")
        if len(parts) >= 2:
            table_name = parts[-2]
            column_name = parts[-1]

            if (
                table_name in self.tables.keys()
                and column_name in self.tables[table_name].columns
            ):
                # We're all good here
                return column

            # logger.error(f"Failed to reolve column {column}")
            return None

        # There is exactly one part, ie. the column name
        # First check if the column if a star
        if column == "*":
            # TODO: Figure out how to handle this
            # assert possible_tables == 1
            # Just return as is
            return column

        matched_tables = []
        for table in possible_tables:
            # We're assuming that the name of the table is correct.
            if table not in self.tables.keys():
                # Return silently, instead of erroring out.
                # logger.error(f"Table {table} not in DDL {self.name}")
                return None

            if column in self.tables[table].columns:
                # logger.debug(f"Found a match for column {column} in {table}")
                matched_tables.append(table)

        # Now, there should be exactly one match
        assert len(matched_tables) == 1
        return f"{matched_tables[0]}.{column}"
