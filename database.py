import sqlite3
from models import Pokemon

class DatabaseHandler:
    """Handles all database operations for Pokemon"""
    
    def __init__(self, db_path='pokemon_information.db'):
        """Initialize database handler"""
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Initialize the database table if it doesn't exist"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS pokemon 
                         (id INTEGER PRIMARY KEY, name TEXT, type1 TEXT, type2 TEXT, 
                         hp INTEGER, atk INTEGER, def INTEGER, spatk INTEGER, spdef INTEGER, speed INTEGER, sprites TEXT)""")
        conn.commit()
        conn.close()
    
    def save_pokemon(self, pokemon):
        """Save or update a Pokemon in the database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""INSERT OR REPLACE INTO pokemon (id, name, type1, type2, hp, atk, def, spatk, spdef, speed, sprites) 
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", pokemon.to_db_tuple())
        conn.commit()
        conn.close()
    
    def get_pokemon_by_id(self, pokemon_id):
        """Get a Pokemon by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pokemon WHERE id = ?", (pokemon_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Pokemon.from_db_row(row)
        return None
    
    def get_pokemon_by_name(self, name):
        """Get a Pokemon by name (case-insensitive)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pokemon WHERE LOWER(name) = LOWER(?)", (name,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Pokemon.from_db_row(row)
        return None
    
    def search_pokemon(self, search_term):
        """Search for a Pokemon by ID or name"""
        if search_term.isdigit():
            return self.get_pokemon_by_id(int(search_term))
        else:
            return self.get_pokemon_by_name(search_term)
    
    def get_all_pokemon_ids_and_names(self):
        """Get all Pokemon IDs and names from database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM pokemon ORDER BY id")
        rows = cursor.fetchall()
        conn.close()
        return rows
