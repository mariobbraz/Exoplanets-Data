import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

DB_PATH = DATA_DIR / "exoplanets.db"

SCHEMA = """
    CREATE TABLE IF NOT EXISTS exoplanets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pl_name TEXT UNIQUE,
        disc_year INTEGER,
        disc_pubdate TEXT,
        sy_dist REAL,
        discoverymethod TEXT,
        pl_orbper REAL,
        pl_orbsmax REAL,
        pl_rade REAL,
        pl_masse REAL,
        pl_eqt REAL,
        pl_insol REAL,
        st_teff REAL,
        st_mass REAL,
        st_rad REAL
    );
    """


def create_database():
    DATA_DIR.mkdir(exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA)
    conn.close()

    print("Database created successfully.")


if __name__ == "__main__":
    create_database()
