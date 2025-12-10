import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, scrolledtext
from PIL import Image, ImageTk
from database import DatabaseHandler
import io

class SelectorFrame(tk.Frame):
    def __init__(self, parent, pokemon, teambuilder):
        super().__init__(parent, bg = "#f0f0f0")
        self.teambuilder = teambuilder
        self.database = DatabaseHandler()

        button_frame = tk.Frame(self, bg="#f0f0f0")
        button_frame.pack(side="top", fill="x", pady=5)

        for column in range(3):
            button_frame.columnconfigure(column, weight=1)
        save_button = tk.Button(
            button_frame,
            command= self.reset,
            text="Save",
            bg="#27ae60",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=5,
            cursor="hand2"
        )
        save_button.grid(row = 0, column = 1)

        selected_pokemon = tk.StringVar()
        rows = self.database.get_all_pokemon_names()

        pokemon_box = ttk.Combobox(
            self,
            width = 30,
            textvariable = selected_pokemon
        )
        pokemon_box['values'] = rows
        pokemon_box.pack()

    def reset(self):
        self.destroy()
        self.teambuilder.show_teambuilder()

