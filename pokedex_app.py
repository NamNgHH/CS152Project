import tkinter as tk
from tkinter import messagebox, scrolledtext
from PIL import Image, ImageTk
import io
from database import DatabaseHandler
from api_handler import PokeAPIHandler

class PokedexApp:
    """Main Pokedex application GUI"""
    
    def __init__(self, root):
        """Initialize the Pokedex application"""
        self.root = root
        self.root.title("Pokédex Application")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f0f0")
        
        self.db_handler = DatabaseHandler()
        self.api_handler = PokeAPIHandler()
        
        self.create_widgets()
        self.refresh_pokemon_list()
    
    def create_widgets(self):
        """Create and configure all GUI widgets"""
        title_label = tk.Label(
            self.root, 
            text="Pokédex", 
            font=("Arial", 24, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        title_label.pack(pady=10)
        
        search_frame = tk.Frame(self.root, bg="#f0f0f0")
        search_frame.pack(pady=10, padx=20, fill="x")
        
        tk.Label(
            search_frame, 
            text="Search Pokemon:", 
            font=("Arial", 12),
            bg="#f0f0f0"
        ).pack(side="left", padx=5)
        
        self.search_entry = tk.Entry(search_frame, font=("Arial", 12), width=20)
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<Return>", lambda e: self.search_pokemon())
        
        search_btn = tk.Button(
            search_frame,
            text="Search",
            command=self.search_pokemon,
            bg="#3498db",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=5,
            cursor="hand2"
        )
        search_btn.pack(side="left", padx=5)
        
        fetch_btn = tk.Button(
            search_frame,
            text="Fetch from API",
            command=self.fetch_pokemon_dialog,
            bg="#27ae60",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=5,
            cursor="hand2"
        )
        fetch_btn.pack(side="left", padx=5)
        
        refresh_btn = tk.Button(
            search_frame,
            text="Refresh List",
            command=self.refresh_pokemon_list,
            bg="#95a5a6",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=5,
            cursor="hand2"
        )
        refresh_btn.pack(side="left", padx=5)
        
        content_frame = tk.Frame(self.root, bg="#f0f0f0")
        content_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        list_frame = tk.Frame(content_frame, bg="white", relief="raised", bd=2)
        list_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        tk.Label(
            list_frame,
            text="Pokemon in Database",
            font=("Arial", 14, "bold"),
            bg="white"
        ).pack(pady=10)
        
        list_scroll = tk.Scrollbar(list_frame)
        list_scroll.pack(side="right", fill="y")
        
        self.pokemon_listbox = tk.Listbox(
            list_frame,
            font=("Arial", 11),
            yscrollcommand=list_scroll.set,
            selectmode=tk.SINGLE
        )
        self.pokemon_listbox.pack(fill="both", expand=True, padx=10, pady=10)
        self.pokemon_listbox.bind("<<ListboxSelect>>", self.on_listbox_select)
        list_scroll.config(command=self.pokemon_listbox.yview)
        
        details_frame = tk.Frame(content_frame, bg="white", relief="raised", bd=2)
        details_frame.pack(side="right", fill="both", expand=True)
        
        tk.Label(
            details_frame,
            text="Pokemon Details",
            font=("Arial", 14, "bold"),
            bg="white"
        ).pack(pady=10)
        
        self.sprite_label = tk.Label(
            details_frame,
            bg="white"
        )
        self.sprite_label.pack(pady=5)
        
        self.details_text = scrolledtext.ScrolledText(
            details_frame,
            font=("Arial", 10),
            wrap=tk.WORD,
            width=40,
            height=15,
            bg="#fafafa"
        )
        self.details_text.pack(fill="both", expand=True, padx=10, pady=10)
    
    def refresh_pokemon_list(self):
        """Refresh the list of Pokemon in the database"""
        self.pokemon_listbox.delete(0, tk.END)
        try:
            rows = self.db_handler.get_all_pokemon_ids_and_names()
            
            for row in rows:
                pokemon_id, name = row
                self.pokemon_listbox.insert(tk.END, f"#{pokemon_id:03d} - {name.capitalize()}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load Pokemon list: {str(e)}")
    
    def search_pokemon(self):
        """Search for a Pokemon by ID or name"""
        search_term = self.search_entry.get().strip()
        if not search_term:
            messagebox.showwarning("Warning", "Please enter a Pokemon ID or name")
            return
        
        try:
            pokemon = self.db_handler.search_pokemon(search_term)
            
            if pokemon:
                self.display_pokemon(pokemon)
                self.select_in_listbox(pokemon.id)
            else:
                messagebox.showinfo("Not Found", f"Pokemon '{search_term}' not found in database.\nTry fetching it from the API first.")
        except Exception as e:
            messagebox.showerror("Error", f"Search failed: {str(e)}")
    
    def select_in_listbox(self, pokemon_id):
        """Select a Pokemon in the listbox by ID"""
        for i in range(self.pokemon_listbox.size()):
            item = self.pokemon_listbox.get(i)
            if item.startswith(f"#{pokemon_id:03d}"):
                self.pokemon_listbox.selection_clear(0, tk.END)
                self.pokemon_listbox.selection_set(i)
                self.pokemon_listbox.see(i)
                break
    
    def on_listbox_select(self, event):
        """Handle listbox selection"""
        selection = self.pokemon_listbox.curselection()
        if selection:
            index = selection[0]
            item = self.pokemon_listbox.get(index)
            pokemon_id = int(item.split(" - ")[0].replace("#", ""))
            self.load_pokemon_by_id(pokemon_id)
    
    def load_pokemon_by_id(self, pokemon_id):
        """Load Pokemon details by ID"""
        try:
            pokemon = self.db_handler.get_pokemon_by_id(pokemon_id)
            
            if pokemon:
                self.display_pokemon(pokemon)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load Pokemon: {str(e)}")
    
    def display_pokemon(self, pokemon):
        """Display Pokemon details in the details area"""
        self.details_text.delete(1.0, tk.END)
        self.sprite_label.config(image="")
        
        details = pokemon.get_formatted_details()
        self.details_text.insert(1.0, details)
        
        self.display_sprite(pokemon)
    
    def display_sprite(self, pokemon):
        """Display Pokemon sprite if available"""
        try:
            sprite_url = pokemon.get_sprite_url()
            if sprite_url:
                image_data = self.api_handler.fetch_sprite_image(sprite_url)
                if image_data:
                    image = Image.open(io.BytesIO(image_data))
                    image = image.resize((150, 150), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(image)
                    self.sprite_label.config(image=photo)
                    self.sprite_label.image = photo
        except Exception as e:
            pass
    
    def fetch_pokemon_dialog(self):
        """Open dialog to fetch Pokemon from API"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Fetch Pokemon from API")
        dialog.geometry("400x200")
        dialog.configure(bg="#f0f0f0")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(
            dialog,
            text="Enter Pokemon ID or name:",
            font=("Arial", 12),
            bg="#f0f0f0"
        ).pack(pady=20)
        
        entry = tk.Entry(dialog, font=("Arial", 12), width=20)
        entry.pack(pady=10)
        entry.focus()
        
        status_label = tk.Label(dialog, text="", bg="#f0f0f0", fg="green")
        status_label.pack(pady=5)
        
        def fetch():
            search_term = entry.get().strip()
            if not search_term:
                status_label.config(text="Please enter an ID or name", fg="red")
                return
            
            status_label.config(text="Fetching...", fg="blue")
            dialog.update()
            
            try:
                pokemon = self.api_handler.fetch_pokemon(search_term)
                self.db_handler.save_pokemon(pokemon)
                status_label.config(text="Successfully fetched!", fg="green")
                self.refresh_pokemon_list()
                dialog.after(1000, dialog.destroy)
            except Exception as e:
                status_label.config(text=f"Error: {str(e)}", fg="red")
        
        fetch_btn = tk.Button(
            dialog,
            text="Fetch",
            command=fetch,
            bg="#27ae60",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=5
        )
        fetch_btn.pack(pady=10)
        
        entry.bind("<Return>", lambda e: fetch())
