import sqlite3
import csv
from pathlib import Path

DB_PATH = Path("data/exoplanets.db")
CSV_PATH = Path("data/nasa_exoplanets.csv")

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

with open(CSV_PATH, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for row in reader:
        cur.execute("""
            INSERT OR IGNORE INTO exoplanets VALUES (
                :pl_name, :disc_year, :disc_pubdate, :sy_dist,
                :discoverymethod, :pl_orbper, :pl_orbsmax,
                :pl_rade, :pl_masse, :pl_eqt, :pl_insol,
                :st_teff, :st_mass, :st_rad
            )
        """, row)

conn.commit()
conn.close()

print("Data loaded.")
