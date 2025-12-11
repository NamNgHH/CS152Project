import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import io
from database import DatabaseHandler
from api_handler import PokeAPIHandler

class DamageCalculator:
    """Pokemon damage calculator window"""
    
    # Type effectiveness chart: attacking_type -> {defending_type: multiplier}
    TYPE_EFFECTIVENESS = {
        'normal': {'rock': 0.5, 'ghost': 0.0, 'steel': 0.5},
        'fire': {'fire': 0.5, 'water': 0.5, 'grass': 2.0, 'ice': 2.0, 'bug': 2.0, 'rock': 0.5, 'dragon': 0.5, 'steel': 2.0},
        'water': {'fire': 2.0, 'water': 0.5, 'grass': 0.5, 'ground': 2.0, 'rock': 2.0, 'dragon': 0.5},
        'electric': {'water': 2.0, 'electric': 0.5, 'grass': 0.5, 'ground': 0.0, 'flying': 2.0, 'dragon': 0.5},
        'grass': {'fire': 0.5, 'water': 2.0, 'grass': 0.5, 'poison': 0.5, 'ground': 2.0, 'flying': 0.5, 'bug': 0.5, 'rock': 2.0, 'dragon': 0.5, 'steel': 0.5},
        'ice': {'fire': 0.5, 'water': 0.5, 'grass': 2.0, 'ice': 0.5, 'ground': 2.0, 'flying': 2.0, 'dragon': 2.0, 'steel': 0.5},
        'fighting': {'normal': 2.0, 'ice': 2.0, 'poison': 0.5, 'flying': 0.5, 'psychic': 0.5, 'bug': 0.5, 'rock': 2.0, 'ghost': 0.0, 'dark': 2.0, 'steel': 2.0, 'fairy': 0.5},
        'poison': {'grass': 2.0, 'poison': 0.5, 'ground': 0.5, 'rock': 0.5, 'ghost': 0.5, 'steel': 0.0, 'fairy': 2.0},
        'ground': {'fire': 2.0, 'electric': 2.0, 'grass': 0.5, 'poison': 2.0, 'flying': 0.0, 'bug': 0.5, 'rock': 2.0, 'steel': 2.0},
        'flying': {'electric': 0.5, 'grass': 2.0, 'fighting': 2.0, 'bug': 2.0, 'rock': 0.5, 'steel': 0.5},
        'psychic': {'fighting': 2.0, 'poison': 2.0, 'psychic': 0.5, 'dark': 0.0, 'steel': 0.5},
        'bug': {'fire': 0.5, 'grass': 2.0, 'fighting': 0.5, 'poison': 0.5, 'flying': 0.5, 'psychic': 2.0, 'ghost': 0.5, 'dark': 2.0, 'steel': 0.5, 'fairy': 0.5},
        'rock': {'fire': 2.0, 'ice': 2.0, 'fighting': 0.5, 'ground': 0.5, 'flying': 2.0, 'bug': 2.0, 'steel': 0.5},
        'ghost': {'normal': 0.0, 'psychic': 2.0, 'ghost': 2.0, 'dark': 0.5},
        'dragon': {'dragon': 2.0, 'steel': 0.5, 'fairy': 0.0},
        'dark': {'fighting': 0.5, 'psychic': 2.0, 'ghost': 2.0, 'dark': 0.5, 'fairy': 0.5},
        'steel': {'fire': 0.5, 'water': 0.5, 'electric': 0.5, 'ice': 2.0, 'rock': 2.0, 'steel': 0.5, 'fairy': 2.0},
        'fairy': {'fire': 0.5, 'fighting': 2.0, 'poison': 0.5, 'dragon': 2.0, 'dark': 2.0, 'steel': 0.5}
    }
    
    def __init__(self, root):
        """Initialize the damage calculator window"""
        self.root = root
        self.root.title("Pokemon Damage Calculator")
        self.root.geometry("800x700")
        self.root.configure(bg="#f0f0f0")
        
        self.db_handler = DatabaseHandler()
        self.api_handler = PokeAPIHandler()
        self.attacker = None
        self.defender = None
        self.selected_move = None
        self.moves_dict = {}  # Maps display name to move tuple
        self.all_moves = []  # Store all moves from database
        
        self.create_widgets()
        self.load_pokemon_list()
        self.load_all_moves()  # Load all moves but don't populate dropdown yet
    
    def go_back(self):
        """Close the damage calculator window"""
        self.root.destroy()
    
    def create_widgets(self):
        """Create and configure all GUI widgets"""
        title_label = tk.Label(
            self.root,
            text="Pokemon Damage Calculator",
            font=("Arial", 24, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        title_label.pack(pady=15)
        
        # Back button
        back_frame = tk.Frame(self.root, bg="#f0f0f0")
        back_frame.pack(pady=5, padx=20, fill="x")
        
        back_btn = tk.Button(
            back_frame,
            text="← Back to Welcome",
            command=self.go_back,
            bg="#95a5a6",
            fg="white",
            font=("Arial", 10),
            padx=15,
            pady=5,
            cursor="hand2"
        )
        back_btn.pack(side="left")
        
        # Main container frame
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Single row selection frame
        selection_frame = tk.LabelFrame(
            main_frame,
            text="Selection",
            font=("Arial", 10, "bold"),
            bg="#f0f0f0",
            padx=10,
            pady=8
        )
        selection_frame.pack(fill="x", pady=5)
        
        # Attacker selection
        attacker_container = tk.Frame(selection_frame, bg="#f0f0f0")
        attacker_container.pack(side="left", padx=10)
        tk.Label(
            attacker_container,
            text="Attacker:",
            font=("Arial", 9),
            bg="#f0f0f0"
        ).pack(side="left", padx=3)
        self.attacker_combo = ttk.Combobox(
            attacker_container,
            font=("Arial", 9),
            width=15,
            state="readonly"
        )
        self.attacker_combo.pack(side="left", padx=3)
        self.attacker_combo.bind("<<ComboboxSelected>>", self.on_attacker_selected)
        
        # Move selection
        move_container = tk.Frame(selection_frame, bg="#f0f0f0")
        move_container.pack(side="left", padx=10)
        tk.Label(
            move_container,
            text="Move:",
            font=("Arial", 9),
            bg="#f0f0f0"
        ).pack(side="left", padx=3)
        self.move_combo = ttk.Combobox(
            move_container,
            font=("Arial", 9),
            width=15,
            state="readonly"
        )
        self.move_combo.pack(side="left", padx=3)
        self.move_combo.bind("<<ComboboxSelected>>", self.on_move_selected)
        
        # Defender selection
        defender_container = tk.Frame(selection_frame, bg="#f0f0f0")
        defender_container.pack(side="left", padx=10)
        tk.Label(
            defender_container,
            text="Defender:",
            font=("Arial", 9),
            bg="#f0f0f0"
        ).pack(side="left", padx=3)
        self.defender_combo = ttk.Combobox(
            defender_container,
            font=("Arial", 9),
            width=15,
            state="readonly"
        )
        self.defender_combo.pack(side="left", padx=3)
        self.defender_combo.bind("<<ComboboxSelected>>", self.on_defender_selected)
        
        # Information row below selection boxes
        info_frame = tk.Frame(main_frame, bg="#f0f0f0")
        info_frame.pack(fill="x", pady=5)
        
        # Attacker info
        attacker_info_container = tk.Frame(info_frame, bg="#f0f0f0")
        attacker_info_container.pack(side="left", padx=20, expand=True)
        tk.Label(
            attacker_info_container,
            text="Attacker:",
            font=("Arial", 9, "bold"),
            bg="#f0f0f0"
        ).pack()
        self.attacker_info_label = tk.Label(
            attacker_info_container,
            text="",
            font=("Arial", 9),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        self.attacker_info_label.pack()
        
        # Move info
        move_info_container = tk.Frame(info_frame, bg="#f0f0f0")
        move_info_container.pack(side="left", padx=20, expand=True)
        tk.Label(
            move_info_container,
            text="Move:",
            font=("Arial", 9, "bold"),
            bg="#f0f0f0"
        ).pack()
        self.move_info_label = tk.Label(
            move_info_container,
            text="(Select a Pokemon first)",
            font=("Arial", 9),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        self.move_info_label.pack()
        
        # Defender info
        defender_info_container = tk.Frame(info_frame, bg="#f0f0f0")
        defender_info_container.pack(side="left", padx=20, expand=True)
        tk.Label(
            defender_info_container,
            text="Defender:",
            font=("Arial", 9, "bold"),
            bg="#f0f0f0"
        ).pack()
        self.defender_info_label = tk.Label(
            defender_info_container,
            text="",
            font=("Arial", 9),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        self.defender_info_label.pack()
        
        # Results frame
        results_frame = tk.LabelFrame(
            main_frame,
            text="Damage Calculation Results",
            font=("Arial", 12, "bold"),
            bg="#f0f0f0",
            padx=10,
            pady=10
        )
        results_frame.pack(fill="both", expand=True, pady=5)
        
        # Pokemon sprites frame
        sprites_frame = tk.Frame(results_frame, bg="#f0f0f0")
        sprites_frame.pack(pady=15, expand=True)
        
        # Attacker sprite
        attacker_sprite_frame = tk.Frame(sprites_frame, bg="#f0f0f0")
        attacker_sprite_frame.pack(side="left", padx=30, expand=True)
        tk.Label(
            attacker_sprite_frame,
            text="Attacker",
            font=("Arial", 12, "bold"),
            bg="#f0f0f0"
        ).pack()
        self.attacker_sprite_label = tk.Label(
            attacker_sprite_frame,
            bg="#f0f0f0"
        )
        self.attacker_sprite_label.pack()
        
        # Defender sprite
        defender_sprite_frame = tk.Frame(sprites_frame, bg="#f0f0f0")
        defender_sprite_frame.pack(side="left", padx=30, expand=True)
        tk.Label(
            defender_sprite_frame,
            text="Defender",
            font=("Arial", 12, "bold"),
            bg="#f0f0f0"
        ).pack()
        self.defender_sprite_label = tk.Label(
            defender_sprite_frame,
            bg="#f0f0f0"
        )
        self.defender_sprite_label.pack()
        
        # Results text area (simplified for damage range only)
        self.results_text = tk.Text(
            results_frame,
            font=("Arial", 18, "bold"),
            wrap=tk.WORD,
            bg="white",
            relief="sunken",
            bd=2,
            padx=10,
            pady=15,
            height=3
        )
        self.results_text.pack(fill="x", pady=15)
    
    def load_pokemon_list(self):
        """Load all Pokemon from database into combo boxes"""
        try:
            rows = self.db_handler.get_all_pokemon_ids_and_names()
            pokemon_list = [f"#{pokemon_id:03d} - {name.capitalize()}" for pokemon_id, name in rows]
            
            self.attacker_combo['values'] = pokemon_list
            self.defender_combo['values'] = pokemon_list
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load Pokemon list: {str(e)}")
    
    def load_all_moves(self):
        """Load all moves from database into memory"""
        try:
            self.all_moves = self.db_handler.get_all_moves()
            if not self.all_moves:
                self.move_combo['values'] = ["No moves found in database"]
                self.move_info_label.config(text="Run fetch_pokemon.py to load moves")
        except Exception as e:
            self.all_moves = []
    
    def load_moves_for_pokemon(self, pokemon_id):
        """Load moves for a specific Pokemon from database or API"""
        # Show loading message
        self.move_combo['values'] = ["Loading moves..."]
        self.move_info_label.config(text="Loading Pokemon moves...")
        self.root.update()
        
        try:
            # First, try to get moves from pokemon_moves table
            pokemon_moves = self.db_handler.get_pokemon_moves(pokemon_id)
            
            move_list = []
            self.moves_dict = {}
            moves_from_db = 0
            moves_from_api = 0
            
            if pokemon_moves:
                # Use moves from pokemon_moves table
                for move in pokemon_moves:
                    move_id, move_name_db, accuracy, power, pp, priority, effect, move_class, move_type = move
                    move_display = f"{move_name_db.capitalize().replace('-', ' ')}"
                    if power:
                        move_display += f" [P:{power}]"
                    move_list.append(move_display)
                    self.moves_dict[move_display] = move
                    moves_from_db += 1
            else:
                # Fallback: Fetch from API if pokemon_moves table is empty
                pokemon_move_names = self.api_handler.fetch_pokemon_moves(pokemon_id)
                
                if not pokemon_move_names:
                    self.move_combo['values'] = ["No moves found for this Pokemon"]
                    self.move_info_label.config(text="Could not fetch moves")
                    return
                
                # Match Pokemon moves with moves in database, and fetch from API if not found
                db_move_names = {move[1]: move for move in self.all_moves}  # Create dict for faster lookup
                
                for pokemon_move_name in pokemon_move_names:
                    move = None
                    if pokemon_move_name in db_move_names:
                        # Move found in database
                        move = db_move_names[pokemon_move_name]
                        moves_from_db += 1
                    else:
                        # Try to fetch move details from API
                        try:
                            self.root.update()
                            move_details = self.api_handler.fetch_move_details(pokemon_move_name)
                            if move_details:
                                move = move_details
                                moves_from_api += 1
                        except Exception:
                            continue  # Skip moves that can't be fetched
                    
                    if move:
                        move_id, move_name_db, accuracy, power, pp, priority, effect, move_class, move_type = move
                        move_display = f"{move_name_db.capitalize().replace('-', ' ')}"
                        if power:
                            move_display += f" [P:{power}]"
                        move_list.append(move_display)
                        self.moves_dict[move_display] = move  # Store mapping
            
            if not move_list:
                self.move_combo['values'] = ["No moves found"]
                self.move_info_label.config(text=f"Could not load moves for this Pokemon")
                return
            
            # Sort moves by name for easier selection
            move_list.sort()
            self.move_combo['values'] = move_list
            self.move_combo.set(move_list[0])
            
            # Update info label
            info_text = f"{len(move_list)} moves available"
            if moves_from_api > 0:
                info_text += f" ({moves_from_db} from DB, {moves_from_api} from API)"
            self.move_info_label.config(text=info_text)
            
            # Trigger selection to load first move
            self.on_move_selected(None)
            
        except Exception as e:
            self.move_combo['values'] = [f"Error: {str(e)}"]
            self.move_info_label.config(text="Failed to fetch moves")
            messagebox.showerror("Error", f"Failed to load Pokemon moves: {str(e)}")
    
    def on_attacker_selected(self, event):
        """Handle attacker selection"""
        selection = self.attacker_combo.get()
        if selection:
            pokemon_id = int(selection.split(" - ")[0].replace("#", ""))
            self.attacker = self.db_handler.get_pokemon_by_id(pokemon_id)
            if self.attacker:
                info = f"Type: {self.attacker.type1.capitalize()}"
                if self.attacker.type2:
                    info += f" / {self.attacker.type2.capitalize()}"
                info += f" | Atk: {self.attacker.atk} | Sp.Atk: {self.attacker.spatk}"
                self.attacker_info_label.config(text=info)
                
                # Display attacker sprite
                self.display_sprite(self.attacker, self.attacker_sprite_label)
                
                # Load moves for this Pokemon
                self.load_moves_for_pokemon(pokemon_id)
    
    def on_defender_selected(self, event):
        """Handle defender selection"""
        selection = self.defender_combo.get()
        if selection:
            pokemon_id = int(selection.split(" - ")[0].replace("#", ""))
            self.defender = self.db_handler.get_pokemon_by_id(pokemon_id)
            if self.defender:
                info = f"Type: {self.defender.type1.capitalize()}"
                if self.defender.type2:
                    info += f" / {self.defender.type2.capitalize()}"
                info += f" | Def: {self.defender.defense} | Sp.Def: {self.defender.spdef}"
                self.defender_info_label.config(text=info)
                
                # Display defender sprite
                self.display_sprite(self.defender, self.defender_sprite_label)
                
                self.calculate_damage()
    
    def on_move_selected(self, event):
        """Handle move selection"""
        selection = self.move_combo.get()
        if not selection:
            self.selected_move = None
            return
        
        # Check for error/loading messages
        error_messages = [
            "No moves found in database",
            "Loading moves...",
            "No moves found for this Pokemon",
            "No matching moves in database"
        ]
        
        if selection in error_messages or selection.startswith("Error:"):
            self.selected_move = None
            return
        
        # Use dictionary lookup for fast matching
        if selection in self.moves_dict:
            self.selected_move = self.moves_dict[selection]
            move_id, move_name_db, accuracy, power, pp, priority, effect, move_class, move_type = self.selected_move
            
            # Display move info
            info = f"{move_type.capitalize()} | "
            if power:
                info += f"Power: {power} | "
            else:
                info += "Status | "
            info += f"{move_class.capitalize()}"
            self.move_info_label.config(text=info)
            self.calculate_damage()
        else:
            self.selected_move = None
    
    def display_sprite(self, pokemon, label):
        """Display Pokemon sprite if available"""
        try:
            sprite_url = pokemon.get_sprite_url()
            if sprite_url:
                image_data = self.api_handler.fetch_sprite_image(sprite_url)
                if image_data:
                    image = Image.open(io.BytesIO(image_data))
                    image = image.resize((200, 200), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(image)
                    label.config(image=photo)
                    label.image = photo  # Keep a reference
        except Exception as e:
            pass  # Silently fail if sprite can't be loaded
    
    def get_type_effectiveness(self, attack_type, defender_type1, defender_type2=None):
        """Calculate type effectiveness multiplier"""
        multiplier = 1.0
        
        # Check effectiveness against first type
        if attack_type in self.TYPE_EFFECTIVENESS:
            if defender_type1 in self.TYPE_EFFECTIVENESS[attack_type]:
                multiplier *= self.TYPE_EFFECTIVENESS[attack_type][defender_type1]
        
        # Check effectiveness against second type if present
        if defender_type2:
            if attack_type in self.TYPE_EFFECTIVENESS:
                if defender_type2 in self.TYPE_EFFECTIVENESS[attack_type]:
                    multiplier *= self.TYPE_EFFECTIVENESS[attack_type][defender_type2]
        
        return multiplier
    
    def calculate_damage(self):
        """Calculate and display damage"""
        if not self.attacker or not self.defender:
            return
        
        if not self.selected_move:
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(1.0, "Please select a move to calculate damage.")
            return
        
        # Display sprites if not already displayed
        if self.attacker:
            self.display_sprite(self.attacker, self.attacker_sprite_label)
        if self.defender:
            self.display_sprite(self.defender, self.defender_sprite_label)
        
        self.results_text.delete(1.0, tk.END)
        
        # Get move data: (id, name, accuracy, power, pp, priority, effect, class, type)
        move_id, move_name, accuracy, power, pp, priority, effect, move_class, move_type = self.selected_move
        
        # Handle status moves (no damage)
        if not power or power == 0:
            results = "Damage Range: 0 HP\n(Status moves deal no damage)"
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(1.0, results)
            return
        
        base_power = power
        move_type_lower = move_type.lower()
        
        # Determine if physical or special based on move's damage class
        is_physical = move_class.lower() == 'physical'
        is_special = move_class.lower() == 'special'
        
        # Get appropriate attack and defense stats
        if is_physical:
            attack_stat = self.attacker.atk
            defense_stat = self.defender.defense
            stat_type = "Physical"
        elif is_special:
            attack_stat = self.attacker.spatk
            defense_stat = self.defender.spdef
            stat_type = "Special"
        else:
            # Default to physical if unknown
            attack_stat = self.attacker.atk
            defense_stat = self.defender.defense
            stat_type = "Physical"
        
        # Calculate type effectiveness
        effectiveness = self.get_type_effectiveness(
            move_type_lower,
            self.defender.type1,
            self.defender.type2
        )
        
        # Calculate STAB (Same Type Attack Bonus) - 1.5x if move type matches Pokemon type
        stab = 1.0
        if move_type_lower == self.attacker.type1.lower() or (self.attacker.type2 and move_type_lower == self.attacker.type2.lower()):
            stab = 1.5
        
        # Simplified damage formula (based on Pokemon damage calculation)
        # Damage = ((2 * Level / 5 + 2) * Power * A/D) / 50 + 2) * Modifier
        # We'll use level 50 as default
        level = 50
        base_damage = ((2 * level / 5 + 2) * base_power * attack_stat / defense_stat) / 50 + 2
        final_damage = base_damage * effectiveness * stab
        
        # Calculate damage range (with random factor between 0.85 and 1.0)
        min_damage = int(final_damage * 0.85)
        max_damage = int(final_damage * 1.0)
        
        # Calculate percentage of HP
        damage_percent_min = (min_damage / self.defender.hp) * 100
        damage_percent_max = (max_damage / self.defender.hp) * 100
        
        # Format results - only show damage range
        results = f"Damage Range: {min_damage} - {max_damage} HP\n"
        results += f"({damage_percent_min:.1f}% - {damage_percent_max:.1f}% of Defender's HP)"

        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, results)
        self.results_text.config(state="normal")

