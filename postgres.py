from dataclasses import dataclass

from constants import DB_PASSWORD, DB_USERNAME, DEFAULT_DB

import logging
import psycopg2

from psycopg2._psycopg import connection, cursor

logging.basicConfig()
logger = logging.getLogger("Postgres")
logger.setLevel(logging.DEBUG)


@dataclass
class Postgres:
    username: str = DB_USERNAME
    password: str = DB_PASSWORD
    database: str = DEFAULT_DB
    address: str = "localhost:5432"
    db_conn: connection = None
    cur: cursor = None

    def connect(self) -> None:
        self.db_conn = psycopg2.connect(
            f"dbname={self.database} user={self.username} password={self.password} host=localhost"
        )
        self.cur = self.db_conn.cursor()
        logger.info("Connected to Postgres database successfully")

    def execute(self, sql):
        self.cur.execute(sql)
        return self.cursor.fetchall()

    def disconnect(self):
        self.cur.close()
        self.db_conn.close()
