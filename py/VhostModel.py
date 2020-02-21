import sqlite3
import os
from pathlib import Path

_dir_path = os.path.dirname(os.path.realpath(__file__))
_root = Path(_dir_path).parent



class VhostModel:
    def __init__(self):
        self.connection = sqlite3.connect(os.path.join(_root, 'data', 'vhosts.db'))
        self.cursor = self.connection.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS vhosts(
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            name TEXT,
            path TEXT
        )''')
        self.connection.commit()

    def add(self, name, path):
        self.cursor.execute('''
            INSERT INTO vhosts (name, path) VALUES (?, ?)
        ''', [(name, path)])
        self.connection.commit()

    def all(self):
        res = self.cursor.execute('SELECT * from vhosts')
        for rest in self.cursor:
            print(res)

    def closeConnection (self):
        self.connection.close()
