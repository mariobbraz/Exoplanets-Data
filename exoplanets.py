import requests
import csv
import json

response = requests.get(
    "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+*+from+ps&format=csv"
)


# Use the NASA API to get information about exoplanets
def main():
    get_data()
    clean_data()
    convert_to_json()
    closer_exoplanets()


# Get data of exoplanets from the nasa api
def get_data():
    with open("nasa_exoplanets.csv", "w") as f:
        f.write(response.text)


# Get the data with the important data [fieldnames]
def clean_data():
    with open("nasa_exoplanets.csv", "r") as f, open("exoplanets.csv", "w") as file:
        fieldnames = [
            "pl_name",
            "disc_year",
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
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        for row in reader:
            important_data = {field: row[field] for field in fieldnames}
            writer.writerow(important_data)


# Convert the important data to json for readability
def convert_to_json():
    with open("exoplanets.csv", "r") as file:
        reader = csv.DictReader(file)
        json_format = []
        for row in reader:
            json_format.append(row)

    with open("exoplanets.json", "w") as file:
        json.dump(json_format, file, indent=2)


def convert_distances(pars):
    km = (float(pars) * 3.085677581e16) / 1000
    au = float(pars) * 206265
    light_years = float(pars) * 3.26156
    parsecs = float(pars)
    return km, au, light_years, parsecs


def closer_exoplanets():
    with open("exoplanets.json", "r") as file:
        data = json.load(file)
        sorted_data = sorted(
            data,
            key=lambda x: float(x["sy_dist"]) if x["sy_dist"] else 9999)

        close_exoplanets = []
        set_exoplanets = set()

        for row in sorted_data:
            if row["pl_name"] not in set_exoplanets:
                close_exoplanets.append(row)
                set_exoplanets.add(row["pl_name"])

    with open("exoplanets_distance.txt", "w") as file:
        file.write("List of Exoplanets Distance From Earth\n\n")
        for i, exoplanet in enumerate(close_exoplanets, start=1):

            if exoplanet["sy_dist"] and exoplanet["sy_dist"] != 9999:
                km, au, light_years, parsecs = convert_distances(
                    exoplanet["sy_dist"])
                file.write(
                    f"{i}) Name: {exoplanet['pl_name']}: \n"
                    f"\tKM: {km:,.0f} \n"
                    f"\tAU: {au:,.2f} \n"
                    f"\tLight Years: {light_years:,.2f} \n"
                    f"\tParsecs: {parsecs:,.2f}\n")

            else:
                file.write(
                    f"{i}) Name: {exoplanet['pl_name']}: \n\tNo value\n")


def farther_exoplanets():
    with open("exoplanets_distance.txt", "r") as file:
        data = json.load(file)
        sorted_data = sorted(
            data,
            reverse=True,
            key=lambda x: float(x["sy_dist"]) if x["sy_dist"] else 0)

    with open("exoplanets_distance.txt", "w") as file:
        file.write("List of Exoplanets Distance From Earth\n\n")


# if __name__ == "__main__":
    # main()
