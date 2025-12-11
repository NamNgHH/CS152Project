import requests
from models import Pokemon

class PokeAPIHandler:
    """Handles interactions with the PokeAPI"""
    
    def __init__(self, base_url="https://pokeapi.co/api/v2/"):
        """Initialize API handler"""
        self.base_url = base_url
    
    def fetch_pokemon(self, search_term):
        """Fetch Pokemon data from PokeAPI by ID or name"""
        pokemon_url = self.base_url + "pokemon/" + str(search_term).lower()
        
        response = requests.get(pokemon_url)
        if response.status_code == 200:
            pokemon_data = response.json()
            return Pokemon.from_api_data(pokemon_data)
        else:
            raise Exception(f"Failed to retrieve Pokemon: {response.status_code}")
    
    def fetch_sprite_image(self, sprite_url):
        """Fetch sprite image from URL"""
        response = requests.get(sprite_url, timeout=5)
        if response.status_code == 200:
            return response.content
        return None
    
    def fetch_pokemon_moves(self, pokemon_id_or_name):
        """Fetch list of move names that a Pokemon can learn"""
        pokemon_url = self.base_url + "pokemon/" + str(pokemon_id_or_name).lower()
        
        try:
            response = requests.get(pokemon_url, timeout=10)
            if response.status_code == 200:
                pokemon_data = response.json()
                moves = []
                # Extract move names from the moves list
                for move_entry in pokemon_data.get("moves", []):
                    move_name = move_entry["move"]["name"]
                    moves.append(move_name)
                return moves
            else:
                return []
        except Exception as e:
            return []
    
    def fetch_move_details(self, move_name_or_id):
        """Fetch detailed move information from API"""
        move_url = self.base_url + "move/" + str(move_name_or_id).lower()
        
        try:
            response = requests.get(move_url, timeout=10)
            if response.status_code == 200:
                move_data = response.json()
                move_id = int(move_data["id"])
                move_name = str(move_data["name"])
                move_accuracy = int(move_data["accuracy"]) if move_data["accuracy"] is not None else 0
                move_power = int(move_data["power"]) if move_data["power"] is not None else 0
                move_pp = int(move_data["pp"]) if move_data["pp"] is not None else 0
                move_priority = int(move_data["priority"]) if move_data["priority"] is not None else 0
                
                # Get effect text (may not always exist)
                effect_text = ""
                if move_data.get("effect_entries") and len(move_data["effect_entries"]) > 0:
                    effect_text = str(move_data["effect_entries"][0].get("effect", ""))
                
                move_class = str(move_data["damage_class"]["name"])
                move_type = str(move_data["type"]["name"])
                
                # Return as tuple matching database format: (id, name, accuracy, power, pp, priority, effect, class, type)
                return (move_id, move_name, move_accuracy, move_power, move_pp, move_priority, effect_text, move_class, move_type)
            else:
                return None
        except Exception as e:
            return None