import sqlite3
from pathlib import Path

DB_PATH = Path("data/exoplanets.db")
SCHEMA = """
CREATE TABLE IF NOT EXISTS exoplanets (
    pl_name TEXT PRIMARY KEY,
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

conn = sqlite3.connect(DB_PATH)
conn.executescript(SCHEMA)
conn.close()

print("Database created.")
