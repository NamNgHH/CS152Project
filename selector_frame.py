import tkinter as tk
from tkinter import ttk
from tkinter import IntVar
from tkinter import messagebox, scrolledtext
from PIL import Image, ImageTk
from database import DatabaseHandler
from api_handler import PokeAPIHandler
import requests
import io

class SelectorFrame(tk.Frame):
    def __init__(self, parent, pokemon, teambuilder):
        super().__init__(parent, bg = "#f0f0f0")
        self.pokemon_frame = pokemon
        self.teambuilder = teambuilder
        self.database = DatabaseHandler()
        self.api_handler = PokeAPIHandler()

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
        names_row = self.database.get_all_pokemon_ids_and_names()

        pokemon_box = ttk.Combobox(
            self,
            width = 30,
            textvariable = selected_pokemon,
            state="readonly"
        )
        pokemon_box['values'] = names_row
        pokemon_box.pack()
        pokemon_box.bind('<<ComboboxSelected>>', self.load_specific_info)

        self.selected_move_1 = tk.StringVar()
        self.move_box_1 = ttk.Combobox(
            self,
            width = 30,
            textvariable = self.selected_move_1,
            state="readonly"
        )
        self.selected_move_2 = tk.StringVar()

        self.move_box_2 = ttk.Combobox(
            self,
            width = 30,
            textvariable = self.selected_move_2,
            state="readonly"
        )
        self.selected_move_3 = tk.StringVar()
        self.move_box_3 = ttk.Combobox(
            self,
            width = 30,
            textvariable = self.selected_move_3,
            state="readonly"
        )
        self.selected_move_4 = tk.StringVar()
        self.move_box_4 = ttk.Combobox(
            self,
            width = 30,
            textvariable = self.selected_move_4,
            state="readonly"
        )

        self.selected_item = tk.StringVar()
        item_row = self.database.get_items()
        item_box = ttk.Combobox(
            self,
            width = 30,
            textvariable = self.selected_item,
            state="readonly"
        )
        item_box['values'] = item_row
        item_box.pack()
        self.sprite_frame = tk.Frame(self, bg="#f0f0f0")
        self.sprite_label = tk.Label(self.sprite_frame, bg="#f0f0f0")

        self.selected_ability = tk.StringVar()
        self.ability_box = ttk.Combobox(
            self,
            width = 30,
            textvariable = self.selected_ability,
            state="readonly"
        )

        ev_frame = tk.Frame(self, bg="#f0f0f0",relief = "solid", borderwidth= 5)
        ev_frame.pack(side="right", fill="y", pady=5)
        self.total_evs = 508
        ev_count_frame = tk.Frame(ev_frame)
        ev_count_frame.pack()
        self.total_evs_label = tk.Label(
            ev_count_frame,
            text = "Total EVs: 508"
        )
        self.total_evs_label.pack()
        self.current_evs_label = tk.Label(
            ev_count_frame,
            text = "EVs Left: 508"
        )
        self.current_evs_label.pack()

        hp_frame = tk.Frame(ev_frame, relief = "groove", borderwidth= 3)
        hp_frame.pack(side="top", fill="x", pady=5)
        hp_label = tk.Label(
            hp_frame,
            text = "HP:"
        )
        hp_label.pack()
        self.hp_value = IntVar()
        hp_scale = tk.Scale(hp_frame, variable= self.hp_value, from_=0, to= 252, length = 252, orient = "horizontal", command = self.hp_limit)
        hp_scale.pack()

        atk_frame = tk.Frame(ev_frame, relief = "groove", borderwidth= 3)
        atk_frame.pack(side="top", fill="x", pady=5)
        atk_label = tk.Label(
            atk_frame,
            text = "ATK:"
        )
        atk_label.pack()
        self.atk_value = IntVar()
        atk_scale = tk.Scale(atk_frame, variable= self.atk_value, from_=0, to= 252, length = 252, orient = "horizontal", command = self.atk_limit)
        atk_scale.pack()

        def_frame = tk.Frame(ev_frame, relief = "groove", borderwidth= 3)
        def_frame.pack(side="top", fill="x", pady=5)
        def_label = tk.Label(
            def_frame,
            text = "DEF:"
        )
        def_label.pack()
        self.def_value = IntVar()
        def_scale = tk.Scale(def_frame, variable= self.def_value, from_=0, to= 252, length = 252, orient = "horizontal", command = self.def_limit)
        def_scale.pack()

        sp_atk_frame = tk.Frame(ev_frame, relief = "groove", borderwidth= 3)
        sp_atk_frame.pack(side="top", fill="x", pady=5)
        sp_atk_label = tk.Label(
            sp_atk_frame,
            text = "SP ATK:"
        )
        sp_atk_label.pack()
        self.sp_atk_value = IntVar()
        sp_atk_scale = tk.Scale(sp_atk_frame, variable= self.sp_atk_value, from_=0, to= 252, length = 252, orient = "horizontal", command = self.sp_atk_limit)
        sp_atk_scale.pack()

        sp_def_frame = tk.Frame(ev_frame, relief = "groove", borderwidth= 3)
        sp_def_frame.pack(side="top", fill="x", pady=5)
        sp_def_label = tk.Label(
            sp_def_frame,
            text = "SP DEF:"
        )
        sp_def_label.pack()
        self.sp_def_value = IntVar()
        sp_def_scale = tk.Scale(sp_def_frame, variable= self.sp_def_value, from_=0, to= 252, length = 252, orient = "horizontal", command = self.sp_def_limit)
        sp_def_scale.pack()

        speed_frame = tk.Frame(ev_frame, relief = "groove", borderwidth= 3)
        speed_frame.pack(side="top", fill="x", pady=5)
        speed_label = tk.Label(
            speed_frame,
            text = "SPEED:"
        )
        speed_label.pack()
        self.speed_value = IntVar()
        speed_scale = tk.Scale(speed_frame, variable= self.speed_value, from_=0, to= 252, length = 252, orient = "horizontal", command = self.speed_limit)
        speed_scale.pack()


    def reset(self):
        self.teambuilder.show_teambuilder()
        self.pokemon_frame.name = self.pokemon_name
        self.pokemon_frame.pokemon_name.config(text=f"Name: {self.pokemon_name}")
        item = self.selected_item.get()
        self.pokemon_frame.item = item
        self.pokemon_frame.pokemon_item.config(text=f"Item: {item}")
        move_1 = self.selected_move_1.get()
        move_2 = self.selected_move_2.get()
        move_3 = self.selected_move_3.get()
        move_4 = self.selected_move_4.get()
        self.pokemon_frame.move_1 = move_1
        self.pokemon_frame.move_2 = move_2
        self.pokemon_frame.move_3 = move_3
        self.pokemon_frame.move_4 = move_4
        self.pokemon_frame.pokemon_moves.config(text=f"Moves:\n{move_1}\n{move_2}\n{move_3}\n{move_4}")
        self.pokemon_frame.pokemon_sprite.config(image = self.photo)
        ability = self.selected_ability.get()
        self.pokemon_frame.ability = ability
        self.pokemon_frame.pokemon_ability.config(text=f"Item: {ability}")
        self.pokemon_frame.type = self.type[0]
        self.pokemon_frame.hp_ev = self.hp_value.get()
        self.pokemon_frame.atk_ev = self.atk_value.get()
        self.pokemon_frame.def_ev = self.def_value.get()
        self.pokemon_frame.sp_atk_ev = self.sp_atk_value.get()
        self.pokemon_frame.sp_def_ev = self.sp_def_value.get()
        self.pokemon_frame.speed_ev = self.speed_value.get() 
        self.pokemon_frame.pokemon_evs.config(text=f"Evs: " + str(self.hp_value.get()) + " HP, " + 
                                              str(self.atk_value.get()) + " ATK, " + 
                                              str(self.def_value.get()) + " DEF,\n"+ 
                                              str(self.sp_atk_value.get()) + " SP ATK, "+
                                              str(self.sp_def_value.get()) + " SP DEF, " +
                                              str(self.speed_value.get()) + " SPEED, ")


    
    def load_specific_info(self, event):
        pokemon_event = event.widget.get()
        pokemon_id, self.pokemon_name = pokemon_event.split(" ", 1)

        sprite_list = self.database.get_pokemon_sprite(pokemon_id)
        pokemon_sprite = sprite_list[0][0]

        image_data = self.api_handler.fetch_sprite_image(pokemon_sprite)
        image = Image.open(io.BytesIO(image_data))
        image = image.resize((150, 150), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(image)
        self.sprite_label.config(image=self.photo)
        self.sprite_label.image = self.photo

        self.sprite_frame.pack(pady=10)
        self.sprite_label.pack()

        move_info = self.database.get_pokemon_moves(pokemon_id)
        pokemon_moves = []
        for i in range(len(move_info)): 
            pokemon_moves.append(move_info[i][1])
        self.move_box_1.pack()
        self.move_box_2.pack()
        self.move_box_3.pack()
        self.move_box_4.pack()
        self.move_box_1['values'] = pokemon_moves
        self.move_box_2['values'] = pokemon_moves
        self.move_box_3['values'] = pokemon_moves
        self.move_box_4['values'] = pokemon_moves

        ability_list = self.database.get_pokemon_abilities(pokemon_id)
        abilities = ability_list[0]
        abilities = [a for a in abilities if a is not None]
        self.ability_box['values'] = abilities
        self.ability_box.pack()

        self.type = self.database.get_pokemon_type(pokemon_id)

    def hp_limit(self, _=None):
        partial = self.atk_value.get() + self.def_value.get() + self.sp_atk_value.get() + self.sp_def_value.get() + self.speed_value.get()
        if partial + self.hp_value.get() > self.total_evs:
            self.hp_value.set(self.total_evs - partial)
        total = self.total_evs - partial - self.hp_value.get()
        self.current_evs_label.config(text=f"EVs Left: {total}")
    def atk_limit(self, _=None):
        partial = self.hp_value.get() + self.def_value.get() + self.sp_atk_value.get() + self.sp_def_value.get() + self.speed_value.get()
        if partial + self.atk_value.get() > self.total_evs:
            self.atk_value.set(self.total_evs - partial)
        total = self.total_evs - partial - self.atk_value.get()
        self.current_evs_label.config(text=f"EVs Left: {total}")
    def def_limit(self, _=None):
        partial = self.hp_value.get() + self.atk_value.get() + self.sp_atk_value.get() + self.sp_def_value.get() + self.speed_value.get()
        if partial + self.def_value.get() > self.total_evs:
            self.def_value.set(self.total_evs - partial)
        total = self.total_evs - partial - self.def_value.get()
        self.current_evs_label.config(text=f"EVs Left: {total}")
    def sp_atk_limit(self, _=None):
        partial = self.hp_value.get() + self.atk_value.get() + self.def_value.get() + self.sp_def_value.get() + self.speed_value.get()
        if partial + self.sp_atk_value.get() > self.total_evs:
            self.sp_atk_value.set(self.total_evs - partial)
        total = self.total_evs - partial - self.sp_atk_value.get()
        self.current_evs_label.config(text=f"EVs Left: {total}")
    def sp_def_limit(self, _=None):
        partial = self.hp_value.get() + self.atk_value.get() + self.def_value.get() + self.sp_atk_value.get() + self.speed_value.get()
        if partial + self.sp_def_value.get() > self.total_evs:
            self.sp_def_value.set(self.total_evs - partial)
        total = self.total_evs - partial - self.sp_def_value.get()
        self.current_evs_label.config(text=f"EVs Left: {total}")
    def speed_limit(self, _=None):
        partial = self.hp_value.get() + self.atk_value.get() + self.def_value.get() + self.sp_atk_value.get() + self.sp_def_value.get()
        if partial + self.speed_value.get() > self.total_evs:
            self.speed_value.set(self.total_evs - partial)
        total = self.total_evs - partial - self.speed_value.get()
        self.current_evs_label.config(text=f"EVs Left: {total}")
        