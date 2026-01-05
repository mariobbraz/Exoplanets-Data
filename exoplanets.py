"""
Exoplanet data analysis using the NASA Exoplanet Archive.

This module downloads, cleans, and processes exoplanet data,
producing CSV, JSON, and human-readable text outputs with
astronomical and physical unit conversions.
"""

import requests
import csv
import json

from pathlib import Path

EARTH_RADIUS_KM = 6371
EARTH_FLUX_W_M2 = 1361
EARTH_MASS_KG = 5.972e24
SOLAR_MASS_KG = 1.9885e30
PARSEC_M = 3.085677581e16
AU_PER_PARSEC = 206265
LIGHTYEARS_PER_PARSEC = 3.26156
EARTH_YEAR = 365.25
MISSING_VALUE = float("inf")

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)


# Use the NASA API to get information about exoplanets
def main():
    """
    Executes the full exoplanet data analysis pipeline.

    This function orchestrates the complete workflow of the project:
    - Downloads raw exoplanet data from the NASA Exoplanet Archive.
    - Stores the raw data in CSV and JSON formats.
    - Removes duplicate entries.
    - Extracts scientifically relevant fields.
    - Generates sorted datasets and human-readable reports related to:
        * Distance
        * Discovery year and publication date
        * Planetary size and mass
        * Orbital period
        * Stellar mass
        * Incident stellar flux (insolation)

    All outputs are written to the `data/` directory.
    """
    response = fetch_nasa_data()
    get_nasa_data(response)
    nasa_data_json()
    all_data_csv()
    all_data_json()
    clean_csv_data()
    key_data_json()
    exoplanets_distance()
    discovery_year()
    publication_date()
    size_exoplanets()
    orbital_period()
    exoplanets_mass()
    stars_mass()
    insolation()


def fetch_nasa_data():
    """
    Fetches raw exoplanet data from the NASA Exoplanet Archive API.

    The data is retrieved using a TAP query and returned in CSV format.

    Returns
    -------
    requests.Response
        HTTP response object containing the CSV data.

    Raises
    ------
    requests.exceptions.HTTPError
        If the request fails or the server returns an error status.
    """
    response = requests.get(
        "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+*+from+ps&format=csv", timeout=30
    )
    response.raise_for_status()
    return response


def get_nasa_data(response):
    """
    Saves raw exoplanet data retrieved from the NASA API to disk.

    Parameters
    ----------
    response : requests.Response
        Response object containing CSV-formatted exoplanet data.

    Side Effects
    ------------
    Writes the file:
        data/nasa_exoplanets.csv
    """
    with open(DATA_DIR / "nasa_exoplanets.csv", "w", encoding="utf-8") as f:
        f.write(response.text)


def check_duplicates(reader):
    """
    Removes duplicate exoplanet entries based on planet name.

    The function preserves the first occurrence of each planet
    and discards subsequent duplicates.

    Parameters
    ----------
    reader : csv.DictReader
        CSV reader containing exoplanet records.

    Returns
    -------
    list of dict
        List of unique exoplanet records.
    """
    database = []
    set_data = set()
    for row in reader:
        if row["pl_name"] not in set_data:
            database.append(row)
            set_data.add(row['pl_name'])
    return database


def all_data_csv():
    """
    Creates a cleaned CSV file without duplicate exoplanet entries.

    Reads the raw NASA dataset, removes duplicate planets,
    and writes the result to a new CSV file.

    Side Effects
    ------------
    Writes the file:
        data/exoplanets.csv
    """
    with open(DATA_DIR / "nasa_exoplanets.csv", "r", encoding="utf-8") as f, open(DATA_DIR / "exoplanets.csv", "w", encoding="utf-8") as file:
        reader = csv.DictReader(f)
        database = check_duplicates(reader)

        writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
        writer.writeheader()
        for row in database:
            writer.writerow(row)


def clean_csv_data():
    """
    Extracts key scientific fields from the exoplanet dataset.

    The function removes duplicate entries and keeps only
    relevant astrophysical and discovery-related parameters.

    Side Effects
    ------------
    Writes the file:
        data/key_exoplanets.csv
    """
    with open(DATA_DIR / "nasa_exoplanets.csv", "r", encoding="utf-8") as f, open(DATA_DIR / "key_exoplanets.csv", "w", encoding="utf-8") as file:
        fieldnames = [
            "pl_name",
            "disc_year",
            "disc_pubdate",
            "sy_dist",
            "discoverymethod",
            "pl_orbper",
            "pl_orbsmax",
            "pl_rade",
            "pl_masse",
            "pl_eqt",
            "pl_insol",
            "st_teff",
            "st_mass",
            "st_rad",
        ]
        reader = csv.DictReader(f)
        database = check_duplicates(reader)

        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in database:
            important_data = {field: row[field] for field in fieldnames}
            writer.writerow(important_data)


def write_json(reader, file):
    """
    Converts CSV data to JSON format and writes it to disk.

    Parameters
    ----------
    reader : csv.DictReader
        Reader containing CSV-formatted data.
    file : pathlib.Path or str
        Output JSON file path.
    """
    json_format = []
    for row in reader:
        json_format.append(row)

    with open(file, "w", encoding="utf-8") as f:
        json.dump(json_format, f, indent=2)


def nasa_data_json():
    """
    Converts the raw NASA exoplanet CSV dataset to JSON format.

    Side Effects
    ------------
    Writes the file:
        data/nasa_exoplanets.json
    """
    with open(DATA_DIR / "nasa_exoplanets.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        write_json(reader, DATA_DIR / "nasa_exoplanets.json")


#####
def all_data_json():
    """
    Converts the deduplicated exoplanet CSV dataset to JSON format.

    Side Effects
    ------------
    Writes the file:
        data/exoplanets.json
    """
    with open(DATA_DIR / "exoplanets.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        write_json(reader, DATA_DIR / "exoplanets.json")


def key_data_json():
    """
    Converts the cleaned and filtered exoplanet dataset to JSON format.

    Side Effects
    ------------
    Writes the file:
        data/key_exoplanets.json
    """
    with open(DATA_DIR / "key_exoplanets.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        write_json(reader, DATA_DIR / "key_exoplanets.json")


def sort_data(funct):
    """
    Sorts exoplanet data using a custom sorting function.

    Parameters
    ----------
    funct : callable
        Function used as sorting key.

    Returns
    -------
    list of dict
        Sorted list of unique exoplanet records.
    """
    with open(DATA_DIR / "key_exoplanets.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        sorted_data = sorted(data, key=funct)

        database = []
        set_data = set()

        for row in sorted_data:
            if row["pl_name"] not in set_data:
                database.append(row)
                set_data.add(row['pl_name'])
    return database


def exoplanets_distance():
    """
    Generates a distance-based report of exoplanets relative to Earth.

    Distances are converted and displayed in:
    - Kilometers
    - Astronomical Units (AU)
    - Light-years
    - Parsecs

    Side Effects
    ------------
    Writes the file:
        data/exoplanets_distance.txt
    """
    def funct(x): return float(x['sy_dist']) if x['sy_dist'] else MISSING_VALUE
    data = sort_data(funct)

    with open(DATA_DIR / "exoplanets_distance.txt", "w", encoding="utf-8") as file:
        file.write("List of Exoplanets Distance From Earth\n\n")
        for i, exoplanet in enumerate(data, start=1):
            if exoplanet['sy_dist'] and exoplanet['sy_dist'] != MISSING_VALUE:

                km = (float(exoplanet['sy_dist']) * PARSEC_M) / 1000
                au = float(exoplanet['sy_dist']) * AU_PER_PARSEC
                light_years = float(
                    exoplanet['sy_dist']) * LIGHTYEARS_PER_PARSEC
                parsecs = float(exoplanet['sy_dist'])

                file.write(
                    f"{i}) Name: {exoplanet['pl_name']}: \n"
                    f"\tKM: {km:,.0f} \n"
                    f"\tAU: {au:,.0f} \n"
                    f"\tLight Years: {light_years:,.2f} \n"
                    f"\tParsecs: {parsecs:,.2f}\n")
            else:
                file.write(f"{i}) Name: {exoplanet['pl_name']}: \n\tNo data\n")


def discovery_year():  # disc_year
    """
    Generates a report of exoplanets sorted by discovery year.

    Side Effects
    ------------
    Writes the file:
        data/exoplanets_discovery.txt
    """
    def funct(x): return float(x['disc_year']
                               ) if x['disc_year'] else MISSING_VALUE
    data = sort_data(funct)

    with open(DATA_DIR / "exoplanets_discovery.txt", "w", encoding="utf-8") as file:
        file.write("List of Exoplanets Discover Years in Order\n\n")
        for i, exoplanet in enumerate(data, start=1):
            if exoplanet['disc_year'] and exoplanet['disc_year'] != MISSING_VALUE:
                file.write(
                    f"{i}) Name: {exoplanet['pl_name']}: \n"
                    f"\tDiscovery Year: {exoplanet['disc_year']}\n")
            else:
                file.write(f"{i}) Name: {exoplanet['pl_name']}: \n\tNo data\n")


def publication_date():  # disc_pubdate
    """
    Generates a report of exoplanets sorted by publication date.

    Side Effects
    ------------
    Writes the file:
        data/exoplanets_publication.txt
    """
    def funct(
        x): return x['disc_pubdate'] if x['disc_pubdate'] else "9999-12-31"
    data = sort_data(funct)

    with open(DATA_DIR / "exoplanets_publication.txt", "w", encoding="utf-8") as file:
        file.write("List of Exoplanets Publication Date in Order\n\n")
        for i, exoplanet in enumerate(data, start=1):
            if exoplanet['disc_pubdate'] and exoplanet['disc_pubdate'] != "9999-12-31":
                file.write(
                    f"{i}) Name: {exoplanet['pl_name']}: \n"
                    f"\tPublication Date: {exoplanet['disc_pubdate']}\n")
            else:
                file.write(f"{i}) Name: {exoplanet['pl_name']}: \n\tNo data\n")


def size_exoplanets():  # pl_rade
    """
    Generates a report of exoplanets sorted by planetary radius.

    Planetary sizes are expressed in:
    - Earth radii (R⊕)
    - Kilometers

    Side Effects
    ------------
    Writes the file:
        data/exoplanets_size.txt
    """
    def funct(x): return float(x['pl_rade']) if x['pl_rade'] else MISSING_VALUE
    data = sort_data(funct)

    with open(DATA_DIR / "exoplanets_size.txt", "w", encoding="utf-8") as file:
        file.write("List of Exoplanets Size From Smaller to Biggest\n\n")
        for i, exoplanet in enumerate(data, start=1):
            if exoplanet['pl_rade'] and exoplanet['pl_rade'] != MISSING_VALUE:
                exoplanet_radius = float(
                    exoplanet['pl_rade']) * EARTH_RADIUS_KM
                file.write(
                    f"{i}) Name: {exoplanet['pl_name']}: \n"
                    f"\tRadius (R⊕): {float(exoplanet['pl_rade']):,.2f} \n"
                    f"\tRadius (km): {exoplanet_radius:,.0f} \n")
            else:
                file.write(f"{i}) Name: {exoplanet['pl_name']}: \n\tNo data\n")


def orbital_period():  # pl_orbper
    """
    Generates a report of exoplanets sorted by orbital period.

    Orbital periods are displayed in:
    - Days
    - Earth years

    Periods longer than 10,000 days are marked as estimated.

    Side Effects
    ------------
    Writes the file:
        data/exoplanets_orbital_period.txt
    """
    def funct(x): return float(x['pl_orbper']
                               ) if x['pl_orbper'] else MISSING_VALUE
    data = sort_data(funct)

    with open(DATA_DIR / "exoplanets_orbital_period.txt", "w", encoding="utf-8") as file:
        file.write("List of Exoplanets Orbital Period\n\n")
        for i, exoplanet in enumerate(data, start=1):
            if exoplanet['pl_orbper'] and exoplanet['pl_orbper'] != MISSING_VALUE:
                if float(exoplanet['pl_orbper']) < 10_000:
                    earth_years = float(exoplanet['pl_orbper']) / EARTH_YEAR
                    file.write(
                        f"{i}) Name: {exoplanet['pl_name']}: \n"
                        f"\tOrbital Period (days): {float(exoplanet['pl_orbper']):,.2f} \n"
                        f"\tEarth Years: {earth_years:,.4f} \n")

                elif exoplanet['pl_orbper'] and float(exoplanet['pl_orbper']) > 10_000:
                    earth_years = float(exoplanet['pl_orbper']) / EARTH_YEAR
                    file.write(
                        f"{i}) Name: {exoplanet['pl_name']}: \n"
                        f"\tOrbital Period (days): (estimated) {float(exoplanet['pl_orbper']):,.2f} \n"
                        f"\tEarth Years: (estimated) {earth_years:,.4f} \n")

            else:
                file.write(
                    f"{i}) Name: {exoplanet['pl_name']}: \n\tNo data \n")


def exoplanets_mass():  # pl_masse
    """
    Generates a report of exoplanets sorted by planetary mass.

    Mass values are expressed in:
    - Earth masses (M⊕)
    - Kilograms

    Side Effects
    ------------
    Writes the file:
        data/exoplanets_mass.txt
    """
    def funct(x): return float(
        x['pl_masse']) if x['pl_masse'] else MISSING_VALUE
    data = sort_data(funct)

    with open(DATA_DIR / "exoplanets_mass.txt", "w", encoding="utf-8") as file:
        file.write("List of Exoplanets Mass in Order \n\n")
        for i, exoplanet in enumerate(data, start=1):
            if exoplanet['pl_masse'] and exoplanet['pl_masse'] != MISSING_VALUE:
                mass_kg = (float(exoplanet['pl_masse']) * EARTH_MASS_KG)
                file.write(
                    f"{i}) Name: {exoplanet['pl_name']}: \n"
                    f"\tMass (M⊕​): {float(exoplanet['pl_masse']):,.2f} \n"
                    f"\tMass (kg): {mass_kg:,.0f} \n")
            else:
                file.write(
                    f"{i}) Name: {exoplanet['pl_name']}: \n\tNo data \n")


def stars_mass():  # st_mass
    """
    Generates a report of host star masses.

    Stellar masses are expressed in:
    - Solar masses (M☉)
    - Kilograms
    - Earth masses (M⊕)

    Side Effects
    ------------
    Writes the file:
        data/exoplanets_star_mass.txt
    """
    def funct(x): return float(
        x['st_mass']) if x['st_mass'] else MISSING_VALUE
    data = sort_data(funct)

    with open(DATA_DIR / "exoplanets_star_mass.txt", "w", encoding="utf-8") as file:
        file.write("List of Exoplanets Star's Mass in Order \n\n")
        for i, exoplanet in enumerate(data, start=1):
            if exoplanet['st_mass'] and exoplanet['st_mass'] != MISSING_VALUE:
                mass_kg = (
                    float(exoplanet['st_mass']) * SOLAR_MASS_KG)
                planet_mass = mass_kg / EARTH_MASS_KG
                file.write(
                    f"{i}) Name: {exoplanet['pl_name']}: \n"
                    f"\tStellar Mass (M☉): {float(exoplanet['st_mass']):,.3f} \n"
                    f"\tMass (kg): {mass_kg:,.0f} \n"
                    f"\tPlanet Mass (M⊕​): {planet_mass:,.0f} \n")

            else:
                file.write(
                    f"{i}) Name: {exoplanet['pl_name']}: \n\tNo data \n")


def insolation():  # pl_insol
    """
    Generates a report of incident stellar flux on exoplanets.

    Insolation values are expressed in:
    - Earth insolation units (S⊕)
    - Watts per square meter (W/m²)

    Side Effects
    ------------
    Writes the file:
        data/exoplanets_insolation.txt
    """
    def funct(x): return float(
        x['pl_insol']) if x['pl_insol'] else MISSING_VALUE
    data = sort_data(funct)

    with open(DATA_DIR / "exoplanets_insolation.txt", "w", encoding="utf-8") as file:
        file.write("List of Exoplanets Incident Stellar Flux in Order \n\n")
        for i, exoplanet in enumerate(data, start=1):
            if exoplanet['pl_insol'] and exoplanet['pl_insol'] != MISSING_VALUE:
                wm2 = float(exoplanet['pl_insol']) * EARTH_FLUX_W_M2
                file.write(
                    f"{i}) Name: {exoplanet['pl_name']}: \n"
                    f"\tInsolation (S⊕): {float(exoplanet['pl_insol']):,.4f} \n"
                    f"\tIncident Stellar Flux (W/m²​): {wm2:,.2f} \n")
            else:
                file.write(
                    f"{i}) Name: {exoplanet['pl_name']}: \n\tNo data \n")


if __name__ == "__main__":
    main()
