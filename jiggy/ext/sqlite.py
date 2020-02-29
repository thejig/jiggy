import sqlite3

from jiggy.task import Task


class SQLiteFetch(Task):
    def __init__(
        self,
        name: str,
        db_path: str,
        fetch: str = "all",
        fetch_count: int = 10,
        query: str = None,
        values: tuple = tuple(),
        **kwargs
    ):
        self.name = name
        self.db_path = db_path
        self.fetch = fetch
        self.fetch_count = fetch_count
        self.query = query
        self.values = values

    def run(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        cur.execute(self.query, self.values)

        if self.fetch == 'all':
            records = cur.fetchall()
        elif self.fetch == 'many':
            records = cur.fetchmany(self.fetch_count)
        else:
            records = cur.fetchone()

        cur.close()
        conn.close()

        return records


class SQLiteExecute(Task):
    def __init__(
        self,
        name: str,
        db_path: str,
        query: str = None,
        values: tuple = tuple(),
        **kwargs
    ):
        self.name = name
        self.db_path = db_path
        self.query = query
        self.values = values

    def run(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        cur.execute(self.query, self.values)

        cur.close()
        conn.close()

        return