import requests
import csv
import json

response = requests.get(
    "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+*+from+ps&format=csv"
)


# Use the NASA API to get information about exoplanets
def main():
    get_nasa_data()
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


def get_nasa_data():
    with open("nasa_exoplanets.csv", "w") as f:
        f.write(response.text)


def check_duplicates(reader):
    database = []
    set_data = set()
    for row in reader:
        if row["pl_name"] not in set_data:
            database.append(row)
            set_data.add(row['pl_name'])
    return database


####
def all_data_csv():
    with open("nasa_exoplanets.csv", "r") as f, open("exoplanets.csv", "w") as file:
        reader = csv.DictReader(f)
        database = check_duplicates(reader)

        writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
        writer.writeheader()
        for row in database:
            writer.writerow(row)


def clean_csv_data():
    with open("nasa_exoplanets.csv", "r") as f, open("key_exoplanets.csv", "w") as file:
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
    json_format = []
    for row in reader:
        json_format.append(row)

    with open(file, "w") as f:
        json.dump(json_format, f, indent=2)


def nasa_data_json():
    with open("nasa_exoplanets.csv", "r") as f:
        reader = csv.DictReader(f)
        write_json(reader, "nasa_exoplanets.json")


#####
def all_data_json():
    with open("exoplanets.csv", "r") as f:
        reader = csv.DictReader(f)
        write_json(reader, "exoplanets.json")


def key_data_json():
    with open("key_exoplanets.csv", "r") as f:
        reader = csv.DictReader(f)
        write_json(reader, "key_exoplanets.json")


def sort_data(funct):
    with open("key_exoplanets.json", "r") as file:
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
    def funct(x): return float(x['sy_dist']) if x['sy_dist'] else 9999
    data = sort_data(funct)

    with open("exoplanets_distance.txt", "w") as file:
        file.write("List of Exoplanets Distance From Earth\n\n")
        for i, exoplanet in enumerate(data, start=1):
            if exoplanet['sy_dist'] and exoplanet['sy_dist'] != 9999:

                km = (float(exoplanet['sy_dist']) * 3.085677581e16) / 1000
                au = float(exoplanet['sy_dist']) * 206265
                light_years = float(exoplanet['sy_dist']) * 3.26156
                parsecs = float(exoplanet['sy_dist'])

                file.write(
                    f"{i}) Name: {exoplanet['pl_name']}: \n"
                    f"\tKM: {km:,.0f} \n"
                    f"\tAU: {au:,.2f} \n"
                    f"\tLight Years: {light_years:,.2f} \n"
                    f"\tParsecs: {parsecs:,.2f}\n")
            else:
                file.write(f"{i}) Name: {exoplanet['pl_name']}: \n\tNo data\n")


def discovery_year():  # disc_year
    def funct(x): return float(x['disc_year']) if x['disc_year'] else 9999
    data = sort_data(funct)

    with open("exoplanets_discovery.txt", "w") as file:
        file.write("List of Exoplanets Discover Years in Order\n\n")
        for i, exoplanet in enumerate(data, start=1):
            if exoplanet['disc_year'] and exoplanet['disc_year'] != 9999:
                file.write(
                    f"{i}) Name: {exoplanet['pl_name']}: \n"
                    f"\tDiscovery Year: {exoplanet['disc_year']}\n")
            else:
                file.write(f"{i}) Name: {exoplanet['pl_name']}: \n\tNo data\n")


def publication_date():  # disc_pubdate
    def funct(
        x): return x['disc_pubdate'] if x['disc_pubdate'] else "9999-12-31"
    data = sort_data(funct)

    with open("exoplanets_publication.txt", "w") as file:
        file.write("List of Exoplanets Publication Date in Order\n\n")
        for i, exoplanet in enumerate(data, start=1):
            if exoplanet['disc_pubdate'] and exoplanet['disc_pubdate'] != "9999-12-31":
                file.write(
                    f"{i}) Name: {exoplanet['pl_name']}: \n"
                    f"\tPublication Date: {exoplanet['disc_pubdate']}\n")
            else:
                file.write(f"{i}) Name: {exoplanet['pl_name']}: \n\tNo data\n")


def size_exoplanets():  # pl_rade
    def funct(x): return float(x['pl_rade']) if x['pl_rade'] else 9999
    data = sort_data(funct)

    with open("exoplanets_size.txt", "w") as file:
        file.write("List of Exoplanets Size From Smaller to Biggest\n\n")
        for i, exoplanet in enumerate(data, start=1):
            if exoplanet['pl_rade'] and exoplanet['pl_rade'] != 9999:
                exoplanet_radius = float(exoplanet['pl_rade']) * 6371
                file.write(
                    f"{i}) Name: {exoplanet['pl_name']}: \n"
                    f"\tRadius (R⊕): {float(exoplanet['pl_rade']):,.2f} R⊕ \n"
                    f"\tRadius (km): {exoplanet_radius:,.0f} km\n")
            else:
                file.write(f"{i}) Name: {exoplanet['pl_name']}: \n\tNo data\n")


def orbital_period():  # pl_orbper
    def funct(x): return float(x['pl_orbper']
                               ) if x['pl_orbper'] else 999_999_999_999
    data = sort_data(funct)

    with open("exoplanets_orbital_period.txt", "w") as file:
        file.write("List of Exoplanets Orbital Period\n\n")
        for i, exoplanet in enumerate(data, start=1):
            if exoplanet['pl_orbper'] and exoplanet['pl_orbper'] != 999_999_999_999:
                if float(exoplanet['pl_orbper']) < 10_000:
                    earth_years = float(exoplanet['pl_orbper']) / 365.25
                    file.write(
                        f"{i}) Name: {exoplanet['pl_name']}: \n"
                        f"\tOrbital Period: {float(exoplanet['pl_orbper']):,.2f} \n"
                        f"\tEarth Years: {earth_years:,.4f} \n")

                elif exoplanet['pl_orbper'] and float(exoplanet['pl_orbper']) > 10_000:
                    earth_years = float(exoplanet['pl_orbper']) / 365.25
                    file.write(
                        f"{i}) Name: {exoplanet['pl_name']}: \n"
                        f"\tOrbital Period: (estimated) {float(exoplanet['pl_orbper']):,.2f} \n"
                        f"\tEarth Years: (estimated) {earth_years:,.4f} \n")

            else:
                file.write(
                    f"{i}) Name: {exoplanet['pl_name']}: \n\tNo data \n")


def mass_exoplanets():  # pl_masse
    ...


def star_mass():  # st_mass
    ...


def energy_recieved():  # pl_insol
    ...


if __name__ == "__main__":
    main()
