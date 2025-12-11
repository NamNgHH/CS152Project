import tkinter as tk
from pokedex_app import PokedexApp
from teambuilder import TeambuilderApp

class WelcomePage:
    """Welcome page for the Pokedex application"""
    
    def __init__(self, root):
        """Initialize the welcome page"""
        self.root = root
        self.root.title("Pokédex - Welcome")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        self.root.configure(bg="#2c3e50")
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create and configure welcome page widgets"""
        main_frame = tk.Frame(self.root, bg="#2c3e50")
        main_frame.pack(expand=True, fill="both")
        
        title_label = tk.Label(
            main_frame,
            text="Welcome to Pokédex",
            font=("Arial", 32, "bold"),
            bg="#2c3e50",
            fg="#ecf0f1"
        )
        title_label.pack(pady=40)
        
        subtitle_label = tk.Label(
            main_frame,
            text="Your Pokemon Database Application",
            font=("Arial", 16),
            bg="#2c3e50",
            fg="#bdc3c7"
        )
        subtitle_label.pack(pady=10)
        
        button_frame = tk.Frame(main_frame, bg="#2c3e50")
        button_frame.pack(pady=30)
        
        enter_btn = tk.Button(
            button_frame,
            text="Enter Pokédex",
            command=self.open_pokedex,
            bg="#3498db",
            fg="white",
            font=("Arial", 16, "bold"),
            padx=40,
            pady=15,
            cursor="hand2",
            relief="raised",
            bd=3
        )
        enter_btn.pack()
        
        button2 = tk.Button(
            button_frame,
            text="Teambuilder",
            command=self.button2_action,
            bg="#9b59b6",
            fg="white",
            font=("Arial", 12),
            padx=30,
            pady=8,
            cursor="hand2"
        )
        button2.pack(pady=5)
        
        button3 = tk.Button(
            button_frame,
            text="Button 3",
            command=self.button3_action,
            bg="#16a085",
            fg="white",
            font=("Arial", 12),
            padx=30,
            pady=8,
            cursor="hand2"
        )
        button3.pack(pady=5)
        
        exit_btn = tk.Button(
            button_frame,
            text="Exit",
            command=self.root.quit,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 12),
            padx=30,
            pady=8,
            cursor="hand2"
        )
        exit_btn.pack(pady=10)
    
    def open_pokedex(self):
        """Open the main Pokedex application"""
        self.root.destroy()
        pokedex_root = tk.Tk()
        app = PokedexApp(pokedex_root)
        pokedex_root.mainloop()
    
    def button2_action(self):
        """Open the teambuilder"""
        self.root.destroy()
        teambuilder_root = tk.Tk()
        app = TeambuilderApp(teambuilder_root)
        teambuilder_root.mainloop()
    
    def button3_action(self):
        """Placeholder for button 3 action"""
        pass

