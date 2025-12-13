import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, scrolledtext
from PIL import Image, ImageTk
import io

class PokemonFrame(tk.Frame):
    def __init__(self, parent):
        """Initialize the Teambuilder application"""
        super().__init__(
            parent,
            width = 275, 
            height = 225,
            relief = "raised",
            bd = 5,
            bg = "#afa9a9",
        )
        # Creates variables that can be accessed in other files
        self.name = ""
        self.item = ""
        self.move_1 = ""
        self.move_2 = ""
        self.move_3 = ""
        self.move_4 = ""
        self.ability = ""
        self.type = ""
        self.hp_ev = 0
        self.atk_ev = 0
        self.def_ev = 0
        self.sp_atk_ev = 0
        self.sp_def_ev = 0
        self.speed_ev = 0   
        self.grid_propagate(False)
        self.create_widgets()
        
        # Creates a 2 by 8 grid for even spacing
        for column in range(2):
            self.columnconfigure(column, weight=1)

        for row in range(8):
            self.rowconfigure(row, weight=1)

    def create_widgets(self):
        """Creates widgets for the pokemon frame GUI"""
        self.pokemon_name = tk.Label(
            self,
            bg = "#afa9a9",
            text = "Name:"
        )
        self.pokemon_name.grid(row = 0, column = 0, sticky = "nw", padx = 1, pady = 1)
        
        self.pokemon_moves = tk.Label(
            self,
            bg = "#afa9a9",
            text = "Moves:"
        )
        self.pokemon_moves.grid(row = 0, column = 1, sticky = "nw", padx = 1, pady = 1, rowspan= 5)
        
        self.pokemon_sprite = tk.Label(
            self, 
            bg="#ff4f4f"
        )
        self.pokemon_sprite.grid(row = 1, column = 0, sticky = "nsew", padx = 1, pady = 1, rowspan = 4)
        
        self.pokemon_item = tk.Label(
            self,
            bg = "#afa9a9",
            text = "Item:"
        )
        self.pokemon_item.grid(row = 6, column = 1, sticky = "nw", padx = 1, pady = 1)
        self.pokemon_ability = tk.Label(
            self,
            bg = "#afa9a9",
            text = "Ability:"
        )
        self.pokemon_ability.grid(row = 6, column = 0, sticky = "nw", padx = 1, pady = 1)
        self.pokemon_evs = tk.Label(
            self,
            bg = "#afa9a9",
            text = "EVs:"
        )
        self.pokemon_evs.grid(row = 7, column = 0, sticky = "nw", rowspan= 1, padx = 2, pady = 1)