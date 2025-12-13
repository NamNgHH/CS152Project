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
        """Creates widgets for the Teambuilder application"""
        # Creates title
        title_label = tk.Label(
            self.root, 
            text="Teambuilder", 
            font=("Arial", 24, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        )    
        title_label.pack(pady=10)

        # Creates a frame for the whole page
        self.teambuilder_page = tk.Frame(self.root, bg="#f0f0f0")
        self.teambuilder_page.pack(fill="both", expand=True)

        # Creates a frame for the buttons
        button_frame = tk.Frame(self.teambuilder_page, bg="#f0f0f0")
        button_frame.pack(side="top", fill="x", pady=5)

        # Makes the grids of the frame evenly spaced
        for column in range(5):
            button_frame.columnconfigure(column, weight=1)

        # Creates export button
        export_button = tk.Button(
            button_frame,
            text="Export",
            bg="#3498db",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=5,
            cursor="hand2",
            command = self.export_pokepaste
        )
        export_button.grid(row = 0, column = 3)

        # Creates back button
        back_btn = tk.Button(
            button_frame,
            text="Back",
            command=self.go_back,
            bg="#27ae60",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=5,
            cursor="hand2"
        )
        back_btn.grid(row = 0, column = 1)

        # Creates a window for all 6 pokemon of the team
        team_window = tk.Frame(self.teambuilder_page, bg="#ffffff", relief="ridge", borderwidth= 5)
        team_window.pack(expand = True)

        # Creates frames for 6 pokemon
        self.pokemon_1 = PokemonFrame(team_window)
        self.pokemon_2 = PokemonFrame(team_window)
        self.pokemon_3 = PokemonFrame(team_window)
        self.pokemon_4 = PokemonFrame(team_window)
        self.pokemon_5 = PokemonFrame(team_window)
        self.pokemon_6 = PokemonFrame(team_window)
        self.pokemon_1.grid(row = 0, column = 0, padx = 5, pady = 5)
        self.pokemon_2.grid(row = 0, column = 1, padx = 5, pady = 5)
        self.pokemon_3.grid(row = 0, column = 2, padx = 5, pady = 5)
        self.pokemon_4.grid(row = 1, column = 0, padx = 5, pady = 5)
        self.pokemon_5.grid(row = 1, column = 1, padx = 5, pady = 5)
        self.pokemon_6.grid(row = 1, column = 2, padx = 5, pady = 5)
        self.pokemon_1.bind("<Button-1>", self.select_pokemon)
        self.pokemon_2.bind("<Button-1>", self.select_pokemon)
        self.pokemon_3.bind("<Button-1>", self.select_pokemon)
        self.pokemon_4.bind("<Button-1>", self.select_pokemon)
        self.pokemon_5.bind("<Button-1>", self.select_pokemon)
        self.pokemon_6.bind("<Button-1>", self.select_pokemon)

        self.selector_page = tk.Frame(self.root, bg="#f0f0f0")


    def hide_teambuilder(self):
        """Hides the current page teambuilder page"""
        self.teambuilder_page.pack_forget()
        self.selector_page.pack(fill="both", expand=True)

    def show_teambuilder(self):
        """Destroys the selector page to show the teambuilder agan"""
        self.current_selector.destroy()
        self.selector_page.pack_forget()
        self.teambuilder_page.pack(fill="both", expand=True)
    
    def select_pokemon(self, event):
        """Displays the selector page and passes through the Pokemon Frame to be accessed"""
        current_pokemon = event.widget
        self.hide_teambuilder()

        self.current_selector = SelectorFrame(self.selector_page, current_pokemon, self)
        self.current_selector.pack(fill = "both", expand = True)
    
    def export_pokepaste(self):
        """Parses and creates proper syntax for exported pokemon information"""
        """Creates pokepaste.txt text file"""
        pokemon_team = [self.pokemon_1, self.pokemon_2, self.pokemon_3, self.pokemon_4, self.pokemon_5, self.pokemon_6]
        pokepaste = ""
        for pokemon in pokemon_team:
            name = pokemon.name.capitalize()
            ability = pokemon.ability
            ability = self.format_text(ability)
            type = pokemon.type.capitalize()
            item = pokemon.item
            item = self.format_text(item)
            move1 = pokemon.move_1
            move1 = self.format_text(move1)
            move2 = pokemon.move_2
            move2 = self.format_text(move2)
            move3 = pokemon.move_3
            move3 = self.format_text(move3)
            move4 = pokemon.move_4
            move4 = self.format_text(move4)
            pokepaste += name + " @ " + item + "\n"
            pokepaste += "Ability: "+ ability + "\n"
            pokepaste += "Tera Type: " + type + "\n"
            pokepaste += "EVs: " + str(pokemon.hp_ev) + " HP / " + str(pokemon.atk_ev) + " Atk / " + str(pokemon.def_ev) + " Def / " + str(pokemon.sp_atk_ev) + " SpA / " + str(pokemon.sp_def_ev) + " SpD / " + str(pokemon.speed_ev) + " Spe\n"
            pokepaste += "- " + move1 + "\n"
            pokepaste += "- " + move2 + "\n"
            pokepaste += "- " + move3 + "\n"
            pokepaste += "- " + move4 + "\n\n"
            with open("pokepaste.txt", "w") as file:
                file.write(pokepaste)

    def format_text(self, input):
        """Replaces hyphes with spaces and capitalizes"""
        input = ' '.join(input.split('-'))
        input = input.title()
        return input
    
    def go_back(self):
        """Close the teambuilder window"""
        self.root.destroy()