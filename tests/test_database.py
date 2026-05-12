# tests/test_database.py

import sqlite3

def test_database_connection():
    conn = sqlite3.connect("publications.db")

    assert conn is not None