import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, scrolledtext
from PIL import Image, ImageTk
from pokemon_frame import PokemonFrame
from selector_frame import SelectorFrame
import io

class TeambuilderApp:
    """Teambuilder application GUI"""
    
    def __init__(self, root):
        """Initialize the Teambuilder application"""
        self.root = root
        self.root.title("Teambuilder")
        self.root.geometry("900x700")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")
        self.create_widgets()

    def create_widgets(self):
        title_label = tk.Label(
            self.root, 
            text="Teambuilder", 
            font=("Arial", 24, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        )    
        title_label.pack(pady=10)

        self.teambuilder_page = tk.Frame(self.root, bg="#f0f0f0")
        self.teambuilder_page.pack(fill="both", expand=True)

        button_frame = tk.Frame(self.teambuilder_page, bg="#f0f0f0")
        button_frame.pack(side="top", fill="x", pady=5)

        for column in range(5):
            button_frame.columnconfigure(column, weight=1)

        back_button = tk.Button(
            button_frame,
            text="Back",
            bg="#27ae60",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=5,
            cursor="hand2"
        )

        search_btn = tk.Button(
            button_frame,
            text="Export",
            bg="#3498db",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=5,
            cursor="hand2"
        )
        back_button.grid(row = 0, column = 1)
        search_btn.grid(row = 0, column = 3)


        team_window = tk.Frame(self.teambuilder_page, bg="#ffffff")
        team_window.pack(expand = True)

        pokemon_1 = PokemonFrame(team_window)
        pokemon_2 = PokemonFrame(team_window)
        pokemon_3 = PokemonFrame(team_window)
        pokemon_4 = PokemonFrame(team_window)
        pokemon_5 = PokemonFrame(team_window)
        pokemon_6 = PokemonFrame(team_window)
        pokemon_1.grid(row = 0, column = 0, padx = 5, pady = 5)
        pokemon_2.grid(row = 0, column = 1, padx = 5, pady = 5)
        pokemon_3.grid(row = 0, column = 2, padx = 5, pady = 5)
        pokemon_4.grid(row = 1, column = 0, padx = 5, pady = 5)
        pokemon_5.grid(row = 1, column = 1, padx = 5, pady = 5)
        pokemon_6.grid(row = 1, column = 2, padx = 5, pady = 5)
        pokemon_1.bind("<Button-1>", self.select_pokemon)
        pokemon_2.bind("<Button-1>", self.select_pokemon)
        pokemon_3.bind("<Button-1>", self.select_pokemon)
        pokemon_4.bind("<Button-1>", self.select_pokemon)
        pokemon_5.bind("<Button-1>", self.select_pokemon)
        pokemon_6.bind("<Button-1>", self.select_pokemon)

        self.selector_page = tk.Frame(self.root, bg="#f0f0f0")


    def hide_teambuilder(self):
        self.teambuilder_page.pack_forget()
        self.selector_page.pack(fill="both", expand=True)

    def show_teambuilder(self):
        self.selector_page.destroy()
        self.teambuilder_page.pack(fill="both", expand=True)
    
    def select_pokemon(self, event):
        current_pokemon = event.widget
        self.hide_teambuilder()
        current_selector = SelectorFrame(self.selector_page, current_pokemon, self)
        current_selector.pack(fill = "both", expand = True)
