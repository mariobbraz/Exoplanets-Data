import requests
from pathlib import Path

URL = (
    "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
    "?query=select+*+from+ps&format=csv"
)

CSV_PATH = Path("data/nasa_exoplanets.csv")

print("Downloading latest exoplanet data...")

response = requests.get(URL, timeout=60)
response.raise_for_status()

CSV_PATH.parent.mkdir(exist_ok=True)
CSV_PATH.write_text(response.text, encoding="utf-8")

print("CSV updated successfully.")
