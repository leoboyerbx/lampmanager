import sqlite3
import os
from pathlib import Path
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

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
        self.list_store = None

    def add(self, name, path):
        self.cursor.execute("INSERT INTO vhosts (name, path) VALUES (?, ?)", (name, path,))
        self.connection.commit()

    def delete(self, ident):
        self.get_name(ident)
        print('hey')
        #self.connection.commit()

    def get_name(self, ident):
        self.cursor.execute('SELECT name FROM vhosts WHERE id = ?', (ident,))
        print(self.cursor.fetchone())

    def all(self):
        self.cursor.execute('SELECT * from vhosts')
        return list(self.cursor)

    def exists(self, name):
        self.cursor.execute('SELECT * from vhosts WHERE name = ?', (name,))
        return bool(self.cursor.fetchone())

    def get_list_store(self):
        store = Gtk.ListStore(int, str, str)
        for row in self.all():
            store.append(list(row))
        self.list_store = store
        return self.list_store


    def close_connection (self):
        self.connection.close()
