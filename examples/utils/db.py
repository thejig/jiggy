import datetime
import random
import sqlite3
from src.jiggy.task import Task


class CreateTable(Task):
    def __init__(self, name):
        self.name = name

    def run(self):

        db = '/Users/mitchell_bregman/git/jiggy/test.db'
        cnx = sqlite3.connect(db)
        cur = cnx.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS random_number_table (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rand_num INTEGER NOT NULL
            )
        """)

        cnx.commit()
        cur.close()
        cnx.close()


class GetRandomNumber(Task):
    def __init__(self, name):
        self.name = name

    def run(self):
        return random.randint(0, 100)


class PrintNumber(Task):
    def __init__(self, name):
        self.name = name

    def run(self, x):
        print(x)


class PersistDatabase(Task):
    def __init__(self, name):
        self.name = name

    def run(self, x):

        db = '/Users/mitchell_bregman/git/jiggy/test.db'
        cnx = sqlite3.connect(db)
        cur = cnx.cursor()

        cur.execute("""
            INSERT INTO random_number_table(rand_num)
            VALUES(?)
        """, (x,))

        cnx.commit()
        cur.close()
        cnx.close()
