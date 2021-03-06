from dataclasses import dataclass

from constants import DB_PASSWORD, DB_USERNAME, DEFAULT_DB

import psycopg2

from psycopg2._psycopg import connection, cursor

from util import get_logger

logger = get_logger("postgres")


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

        if self.cur.description:
            return self.cur.fetchall()

    def commit(self):
        self.db_conn.commit()

    def disconnect(self):
        self.cur.close()
        self.db_conn.close()
