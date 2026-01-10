import requests
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

CSV_PATH = DATA_DIR / "nasa_exoplanets.csv"

URL = (
    "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
    "?query=select+*+from+ps&format=csv"
)


def update_csv():
    print("Downloading latest exoplanet data...")

    response = requests.get(URL, timeout=60)
    response.raise_for_status()

    DATA_DIR.mkdir(exist_ok=True)
    CSV_PATH.write_text(response.text, encoding="utf-8")

    print("CSV updated successfully.")


if __name__ == "__main__":
    update_csv()
