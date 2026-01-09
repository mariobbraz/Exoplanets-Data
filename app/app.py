import sqlite3
import tkinter as tk
from tkinter import ttk
from pathlib import Path

DB_PATH = Path("data/exoplanets.db")

ALLOWED_ORDER = {
    "name": "pl_name",
    "distance": "sy_dist",
    "size": "pl_rade",
    "insolation": "pl_insol"
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
            columns=("name", "dist", "size", "insol"),
            show="headings"
        )

        self.tree.heading("name", text="Name")
        self.tree.heading("dist", text="Distance (pc)")
        self.tree.heading("size", text="Radius (R⊕)")
        self.tree.heading("insol", text="Insolation (S⊕)")

        self.tree.pack(fill="both", expand=True)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="By Name",
                  command=lambda: self.load_data("name")).pack(side="left")
        tk.Button(btn_frame, text="By Distance",
                  command=lambda: self.load_data("distance")).pack(side="left")
        tk.Button(btn_frame, text="By Size",
                  command=lambda: self.load_data("size")).pack(side="left")
        tk.Button(btn_frame, text="By Insolation",
                  command=lambda: self.load_data("insolation")).pack(side="left")

    def load_data(self, order_key):
        order_by = ALLOWED_ORDER[order_key]

        self.cursor.execute(f"""
                            SELECT pl_name, sy_dist, pl_rade, pl_insol
                            FROM exoplanets
                            ORDER BY {order_by} IS NULL, {order_by}
                            """)

        for row in self.tree.get_children():
            self.tree.delete(row)

        for row in self.cursor.fetchall():
            formatted = [
                value if value is not None else "No value"
                for value in row
            ]
            self.tree.insert("", tk.END, values=formatted)

    def close(self):
        self.conn.close()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ExoplanetApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close)
    root.mainloop()
