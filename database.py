import sqlite3
import pandas as pd

def create_database():
    conn = sqlite3.connect("publication.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS publications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        venue TEXT,
        year INTEGER,
        source TEXT,
        type TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_to_db(df):
    conn = sqlite3.connect("publication.db")
    df.to_sql("publications", conn, if_exists="replace", index=False)
    conn.close()


def load_from_db():
    conn = sqlite3.connect("publication.db")
    df = pd.read_sql("SELECT * FROM publications", conn)
    conn.close()
    return df