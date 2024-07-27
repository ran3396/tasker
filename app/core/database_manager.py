from typing import Optional, List, Dict, Any
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from flask import Config


class DatabaseManager:
    def __init__(self, config: Config) -> None:
        self.config: Config = config

    @contextmanager
    def get_connection(self):
        connection = psycopg2.connect(
            host=self.config['DB_HOST'],
            database=self.config['DB_NAME'],
            user=self.config['DB_USER'],
            password=self.config['DB_PASSWORD'],
            cursor_factory=RealDictCursor
        )
        try:
            yield connection
        finally:
            connection.close()

    def execute(self, query: str, params: Optional[tuple] = None) -> Optional[List[Dict[str, Any]]]:
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                conn.commit()
                if cur.description:
                    return cur.fetchall()
                return None
