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
    exoplanets_mass()
    stars_mass()
    insolation()


def get_nasa_data():
    """
    Get all the data of the NASA exoplanets API in csv format and
    save it in 'nasa_exoplanets.csv'
    """
    with open("nasa_exoplanets.csv", "w") as f:
        f.write(response.text)


def check_duplicates(reader):
    """
    Check if there are duplicates of the explanets and remove them using a
    new list and a set checking by their name
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
    This function clean the duplicates of the API data and save it in
    'exoplanets.csv'
    """
    with open("nasa_exoplanets.csv", "r") as f, open("exoplanets.csv", "w") as file:
        reader = csv.DictReader(f)
        database = check_duplicates(reader)

        writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
        writer.writeheader()
        for row in database:
            writer.writerow(row)


def clean_csv_data():
    """
    Clean the data using only relevant data, remove dulplicates and save it in
    'key_exoplanets.csv'
    """
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
    """
    Make easier to write from csv to json
    """
    json_format = []
    for row in reader:
        json_format.append(row)

    with open(file, "w") as f:
        json.dump(json_format, f, indent=2)


def nasa_data_json():
    """
    Get all the data from 'nasa_exoplanets.csv', convert it to json
    and save it in 'nasa_exoplanets.json'
    """
    with open("nasa_exoplanets.csv", "r") as f:
        reader = csv.DictReader(f)
        write_json(reader, "nasa_exoplanets.json")


#####
def all_data_json():
    """
    Convert the data without duplicates ('exoplanets.csv') from csv to json
    and save it in 'exoplanets.json'
    """
    with open("exoplanets.csv", "r") as f:
        reader = csv.DictReader(f)
        write_json(reader, "exoplanets.json")


def key_data_json():
    """
    Convert the data without duplicates and with key data ('key_exoplanets.csv')
    from csv to json and save it in 'key_exoplanets.json'
    """
    with open("key_exoplanets.csv", "r") as f:
        reader = csv.DictReader(f)
        write_json(reader, "key_exoplanets.json")


def sort_data(funct):
    """
    Sort the exoplanet data using a specified sorting function
    """
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
    """
    Sort and enumerate exoplanets by distance from Earth from 'key_exoplanets.json'
    and formatted in km, au, light years and parsecs and write the formatted
    and sorted data to 'exoplanets_distance.txt' (if no data print no value)
    """
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
                    f"\tAU: {au:,.0f} \n"
                    f"\tLight Years: {light_years:,.2f} \n"
                    f"\tParsecs: {parsecs:,.2f}\n")
            else:
                file.write(f"{i}) Name: {exoplanet['pl_name']}: \n\tNo data\n")


def discovery_year():  # disc_year
    """
    Sort and enumerate the data by discovery year, formatted and save it
    in 'exoplanets_discovery.txt'
    """
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
    """
    Sort and enumerate the data by discovery publication date and formatted
    and save it in 'exoplanets_publication.txt'
    """
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
    """
    Sort and enumerate the data by size in radius and formatted in Earth Radius (R⊕)
    and Radius in km and save it in 'exoplanets_size.txt'
    """
    def funct(x): return float(x['pl_rade']) if x['pl_rade'] else 9999
    data = sort_data(funct)

    with open("exoplanets_size.txt", "w") as file:
        file.write("List of Exoplanets Size From Smaller to Biggest\n\n")
        for i, exoplanet in enumerate(data, start=1):
            if exoplanet['pl_rade'] and exoplanet['pl_rade'] != 9999:
                exoplanet_radius = float(exoplanet['pl_rade']) * 6371
                file.write(
                    f"{i}) Name: {exoplanet['pl_name']}: \n"
                    f"\tRadius (R⊕): {float(exoplanet['pl_rade']):,.2f} \n"
                    f"\tRadius (km): {exoplanet_radius:,.0f} \n")
            else:
                file.write(f"{i}) Name: {exoplanet['pl_name']}: \n\tNo data\n")


def orbital_period():  # pl_orbper
    """
    Sort and enumerate the data by orbital period and formatted in Orbital period (days)
    and Earth years and save it in 'exoplanets_orbital_period.txt'
    (if orbital period > 10000 its most likely and estimate and write it)
    """
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
                        f"\tOrbital Period (days): {float(exoplanet['pl_orbper']):,.2f} \n"
                        f"\tEarth Years: {earth_years:,.4f} \n")

                elif exoplanet['pl_orbper'] and float(exoplanet['pl_orbper']) > 10_000:
                    earth_years = float(exoplanet['pl_orbper']) / 365.25
                    file.write(
                        f"{i}) Name: {exoplanet['pl_name']}: \n"
                        f"\tOrbital Period (days): (estimated) {float(exoplanet['pl_orbper']):,.2f} \n"
                        f"\tEarth Years: (estimated) {earth_years:,.4f} \n")

            else:
                file.write(
                    f"{i}) Name: {exoplanet['pl_name']}: \n\tNo data \n")


def exoplanets_mass():  # pl_masse
    """
    Sort and enumerate the data by exoplanet mass and formatted in Earth mass(M⊕) and
    mass in tons and save it in 'exoplanets_mass.txt'
    """
    def funct(x): return float(
        x['pl_masse']) if x['pl_masse'] else 999_999_999_999
    data = sort_data(funct)

    with open("exoplanets_mass.txt", "w") as file:
        file.write("List of Exoplanets Mass in Order \n\n")
        for i, exoplanet in enumerate(data, start=1):
            if exoplanet['pl_masse'] and exoplanet['pl_masse'] != 999_999_999_999:
                mass_tons = (float(exoplanet['pl_masse']) * 5.972e24) / 1000
                file.write(
                    f"{i}) Name: {exoplanet['pl_name']}: \n"
                    f"\tMass (M⊕​): {float(exoplanet['pl_masse']):,.2f} \n"
                    f"\tMass (tons): {mass_tons:,.0f} \n")
            else:
                file.write(
                    f"{i}) Name: {exoplanet['pl_name']}: \n\tNo data \n")


def stars_mass():  # st_mass
    """
    Sort and enumerate the data by exoplanet's Star mass and formatted in Stellar Mass (M☉),
    Planet mass (M⊕) and mass in tons and save it in 'exoplanets_star_mass.txt'
    """
    def funct(x): return float(
        x['st_mass']) if x['st_mass'] else 999_999_999_999
    data = sort_data(funct)

    with open("exoplanets_star_mass.txt", "w") as file:
        file.write("List of Exoplanets Star's Mass in Order \n\n")
        for i, exoplanet in enumerate(data, start=1):
            if exoplanet['st_mass'] and exoplanet['st_mass'] != 999_999_999_999:
                mass_tons = (float(exoplanet['st_mass']) * 1.9885e30) / 1000
                planet_mass = mass_tons / (5.972e24 / 1000)
                file.write(
                    f"{i}) Name: {exoplanet['pl_name']}: \n"
                    f"\tStellar Mass (M☉): {float(exoplanet['st_mass']):,.3f} \n"
                    f"\tMass (Tons): {mass_tons:,.0f} tons \n"
                    f"\tPlanet Mass (M⊕​): {planet_mass:,.0f} \n")

            else:
                file.write(
                    f"{i}) Name: {exoplanet['pl_name']}: \n\tNo data \n")


def insolation():  # pl_insol
    """
    Sort and enumerate the data by Incident Stellar Flux and formatted in Insolation (S⊕)
    and Incident Stellar Flux (W/m²​) and save it in 'exoplanets_insolation.txt'
    """
    def funct(x): return float(
        x['pl_insol']) if x['pl_insol'] else 999_999_999_999
    data = sort_data(funct)

    with open("exoplanets_insolation.txt", "w") as file:
        file.write("List of Exoplanets Incident Stellar Flux in Order \n\n")
        for i, exoplanet in enumerate(data, start=1):
            if exoplanet['pl_insol'] and exoplanet['pl_insol'] != 999_999_999_999:
                wm2 = float(exoplanet['pl_insol']) * 1361
                file.write(
                    f"{i}) Name: {exoplanet['pl_name']}: \n"
                    f"\tInsolation (S⊕): {float(exoplanet['pl_insol']):,.4f} \n"
                    f"\tIncident Stellar Flux (W/m²​): {wm2:,.2f} \n")
            else:
                file.write(
                    f"{i}) Name: {exoplanet['pl_name']}: \n\tNo data \n")


if __name__ == "__main__":
    main()
