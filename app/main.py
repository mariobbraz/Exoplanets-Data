import sqlite3
import tkinter as tk
import subprocess
import sys

from tkinter import ttk
from tkinter import messagebox
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
SCRIPTS_DIR = BASE_DIR / "scripts"

DB_PATH = DATA_DIR / "exoplanets.db"


ALLOWED_ORDER = {
    "name": "pl_name",
    "distance": "sy_dist",
    "size": "pl_rade",
    "insolation": "pl_insol",
    "mass": "pl_masse",
    "orbital_period": "pl_orbper",
    "discovery_year": "disc_year",
    "publication_date": "disc_pubdate",
    "star_mass": "st_mass"
}


class ExoplanetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Exoplanet Explorer")

        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()

        self.create_widgets()
        self.load_data("name")

    def create_widgets(self):
        self.tree = ttk.Treeview(
            self.root,
            columns=("name", "dist", "size", "insol",
                     "mass", "star_mass", "orbital_period",
                     "discovery_year", "publication_date",
                     ),
            show="headings"
        )

        self.tree.heading("name", text="Name")
        self.tree.heading("dist", text="Distance (pc)")
        self.tree.heading("size", text="Radius (R⊕)")
        self.tree.heading("insol", text="Insolation (S⊕)")
        self.tree.heading("mass", text="Mass (M⊕)")
        self.tree.heading("star_mass", text="Stellar Mass (M☉)")
        self.tree.heading("orbital_period", text="Orbital Period")
        self.tree.heading("discovery_year", text="Discovery Year")
        self.tree.heading("publication_date", text="Publication Date")

        self.tree.pack(fill="both", expand=True)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="By Name",
                  command=lambda: self.load_data("name")
                  ).pack(side="left")
        tk.Button(btn_frame, text="By Distance",
                  command=lambda: self.load_data("distance")
                  ).pack(side="left")
        tk.Button(btn_frame, text="By Size",
                  command=lambda: self.load_data("size")
                  ).pack(side="left")
        tk.Button(btn_frame, text="By Mass",
                  command=lambda: self.load_data("mass")
                  ).pack(side="left")
        tk.Button(btn_frame, text="By Insolation",
                  command=lambda: self.load_data("insolation")
                  ).pack(side="left")
        tk.Button(btn_frame, text="By Orbital Period",
                  command=lambda: self.load_data("orbital_period")
                  ).pack(side="left")
        tk.Button(btn_frame, text="By Discovery Year",
                  command=lambda: self.load_data("discovery_year")
                  ).pack(side="left")
        tk.Button(btn_frame, text="By Publication Date",
                  command=lambda: self.load_data("publication_date")
                  ).pack(side="left")
        tk.Button(btn_frame, text="By Star Mass",
                  command=lambda: self.load_data("star_mass")
                  ).pack(side="left")

        # Update database button
        tk.Button(self.root, text="Update Database",
                  command=self.update_database,
                  ).pack(pady=5)

    def load_data(self, order_key):
        order_by = ALLOWED_ORDER[order_key]

        self.cursor.execute(f"""
                            SELECT pl_name, sy_dist, pl_rade, 
                            pl_insol, pl_masse, st_mass, pl_orbper, 
                            disc_year, disc_pubdate
                            FROM exoplanets
                            ORDER BY {order_by} IS NULL, {order_by}
                            """)

        for row in self.tree.get_children():
            self.tree.delete(row)

        for row in self.cursor.fetchall():
            formatted = [
                value if value is not None else "No value" for value in row
            ]
            self.tree.insert("", tk.END, values=formatted)

    def update_database(self):
        try:
            subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "update_data.py")],
                check=True
            )
            subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "load_data.py")],
                check=True
            )

            messagebox.showinfo(
                "Update complete", "Exoplanet database updated successfully."
            )

            self.load_data("name")

        except subprocess.CalledProcessError:
            messagebox.showerror(
                "Update failed", "Error updating the database."
            )

    def close(self):
        self.conn.close()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ExoplanetApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close)
    root.mainloop()
