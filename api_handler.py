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

