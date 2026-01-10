import sqlite3
import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

DB_PATH = DATA_DIR / "exoplanets.db"
CSV_PATH = DATA_DIR / "nasa_exoplanets.csv"


def load_data():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        conn.execute("BEGIN")

        for row in reader:
            cur.execute("""
                INSERT OR IGNORE INTO exoplanets (
                    pl_name, disc_year, disc_pubdate, sy_dist,
                    discoverymethod, pl_orbper, pl_orbsmax,
                    pl_rade, pl_masse, pl_eqt, pl_insol,
                    st_teff, st_mass, st_rad
                ) VALUES (
                    :pl_name, :disc_year, :disc_pubdate, :sy_dist,
                    :discoverymethod, :pl_orbper, :pl_orbsmax,
                    :pl_rade, :pl_masse, :pl_eqt, :pl_insol,
                    :st_teff, :st_mass, :st_rad
                )
            """, row)

    conn.commit()
    conn.close()

    print("Data loaded successfully.")


if __name__ == "__main__":
    load_data()
