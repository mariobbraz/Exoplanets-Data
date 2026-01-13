# Exoplanet Explorer

**Exoplanet Explorer** is a desktop application that allows interactive exploration of confirmed exoplanets using data from the **NASA Exoplanet Archive**.

The project combines **real scientific data**, a **local SQLite database**, and a **graphical interface built with Tkinter**, enabling users to browse, sort, and update exoplanet information in a clean and accessible way.

The goal of this project is to make exoplanetary science **explorable**, **transparent**, and **hands-on**, while keeping the data pipeline simple and reproducible.

---

## Description

This application downloads the latest confirmed exoplanet data from the **NASA Exoplanet Archive**, stores it locally in a **SQLite database**, and presents it through an interactive graphical interface.

Users can sort exoplanets by multiple physical, orbital, and discovery-related parameters, and update the database at any time directly from the application.

The data pipeline is intentionally split into independent scripts to keep responsibilities clear:

- **Data acquisition** (CSV download)
- **Database creation**
- **Data loading**
- **Data exploration (GUI)**

---

## Features

- Downloads up-to-date exoplanet data from the NASA Exoplanet Archive
- Stores data locally using SQLite
- Interactive graphical interface (Tkinter)
- Sort exoplanets by:
  - Name
  - Distance
  - Radius
  - Mass
  - Insolation
  - Orbital period
  - Discovery year
  - Publication date
  - Stellar mass
- Handles missing scientific values gracefully
- One-click database update from the GUI

---

## Data Source

- **NASA Exoplanet Archive**

https://exoplanetarchive.ipac.caltech.edu/

> No API key is required to access this dataset.

The data is retrieved directly from the `ps` (Planetary Systems) table in CSV format.

---

## Installation

Follow the steps below to run the project locally.

### 1. Clone the repository

```bash
git clone https://github.com/mariobbraz/Exoplanets-Data
cd Exoplanets-Data
```

### 2. Create and activate a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Initial Setup (First Run)

Before launching the application for the first time, you need to create and populate the database.

Run the following scripts once:

```bash
python scripts/create_db.py
python scripts/update_data.py
python scripts/load_data.py
python app/main.py
```

This will:

1. Create the SQLite database
2. Download the latest exoplanet dataset
3. Load the data into the database
4. Start the App

---

## Usage

Start the graphical application:

```bash
python app/main.py
```

### Inside the application

- Use the buttons to sort exoplanets by different parameters
- Click Update Database to:
  - Download the latest data
  - Reload the database automatically
- Close the window safely to ensure the database connection is closed properly

---

## Project Structure

```bash
Exoplanets-Data/
├── app/
│   └── main.py              # Tkinter GUI application
├── scripts/
│   ├── create_db.py         # Creates the SQLite database schema
│   ├── update_data.py       # Downloads latest NASA exoplanet CSV
│   └── load_data.py         # Loads CSV data into the database
├── data/
│   ├── exoplanets.db        # SQLite database
│   └── nasa_exoplanets.csv  # Raw NASA dataset
├── .gitignore
├── requirements.txt
└── README.md

```

---

## Technologies Used

- Python 3
- SQLite
- Tkinter
- Requests
- NASA Exoplanet Archive API

---

## Feedback

If you have feedback, ideas, or suggestions, feel free to open an issue or contact me.
