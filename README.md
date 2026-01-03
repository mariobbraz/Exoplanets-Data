# Exoplanet Data Analyzer

This program is a data processing tool that collects exoplanet data from the **NASA Exoplanet Archive API**, removes duplicates, converts formats, and generates sorted and human-readable outputs using multiple scientific measurement units.

The objective of this project is to better understand the universe and the exoplanets along with their **wide-ranging properties**

## Description

This project retrieves exoplanet data from **NASA exoplanet Archive** in CSV format and processes it into clean, structured datasets.

The program removes duplicate entries, converts CSV data to JSON, and generates multiple sorted text reports based on physical, orbital, and discovery-related properties.
The output is designed to be more readable by converting raw scientific values into commonly used **astronomical and physics units**.

## Features

- Fetches raw exoplanet data from the NASA Exoplanet Archive API
- Removes duplicates exoplanet entries
- Converts CSV data into JSON format
- Filters and stores key scientific parameters
- Sorts and exports exoplanet data into readable text files
- Converts values into multiple measurement units

## Generated Data & Measurement Units

The data is organize and sorted in a variety of different categories, such as:

- **Size** (Radius (Earth radii (R⊕)) - Radius (kilometers (km))
- **Distance from earth** (km - Astronomical Units (AU) - Light Years (ly) - Parsecs (pc))
- **Discovery year**
- **Date of publication** (month/year)
- **Orbital period** (days - Earth years)
- **Mass** (Earth masses (M⊕) - kilograms (kg))
- **Stellar mass** (Stellar mass (M☉) - kg - Earth masses (M⊕))
- **Insolation** (Insolation (S⊕) - Incident stellar flux (W/m²))

## Data Source

- **NASA Exoplanet Archive API**

https://api.nasa.gov/

https://exoplanetarchive.ipac.caltech.edu/

## Installation:

1. Clone the repository:

To run the code in your machine, copy the code or clone the repository

```bash
git clone https://github.com/code50/220114113
cd project
```

2. Create and activate a virtual environment:

This step is optional but recommended

```bash
python -m venv env
source env/bin/activate  # In Windows use `env\Scripts\activate`
```

3. Install dependencies:

To install the requirements, run the following command

```bash
pip install -r requirements.txt
```

## Usage

Run the main script:

```bash
python project.py
```

Once you run the script you will have all the different type of data in .csv, .json and .txt format

## Project Structure

After running the script this will be the structure of the repository

```bash
.
├── project.py
├── test_project.py
├── nasa_exoplanets.csv
├── nasa_exoplanets.json
├── exoplanets.csv
├── exoplanets.json
├── key_exoplanets.csv
├── key_exoplanets.json
├── exoplanets_distance.txt
├── exoplanets_discovery.txt
├── exoplanets_publication.txt
├── exoplanets_size.txt
├── exoplanets_orbital_period.txt
├── exoplanets_mass.txt
├── exoplanets_star_mass.txt
├── exoplanets_insolation.txt
```

## Feedback

If you have feedback to share please message me and
