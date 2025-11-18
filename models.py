class Pokemon:
    """Represents a Pokemon with its data"""
    
    def __init__(self, pokemon_id, name, type1, type2=None, hp=0, atk=0, defense=0, spatk=0, spdef=0, speed=0, sprites=None):
        """Initialize a Pokemon object"""
        self.id = pokemon_id
        self.name = name
        self.type1 = type1
        self.type2 = type2
        self.hp = hp
        self.atk = atk
        self.defense = defense
        self.spatk = spatk
        self.spdef = spdef
        self.speed = speed
        self.sprites = sprites if sprites else ""
    
    @classmethod
    def from_api_data(cls, api_data):
        """Create a Pokemon object from PokeAPI response data"""
        pokemon_id = int(api_data["id"])
        name = str(api_data["name"])
        type1 = str(api_data["types"][0]["type"]["name"])
        type2 = None
        if len(api_data["types"]) > 1:
            type2 = str(api_data["types"][1]["type"]["name"])
        hp = int(api_data["stats"][0]["base_stat"])
        atk = int(api_data["stats"][1]["base_stat"])
        defense = int(api_data["stats"][2]["base_stat"])
        spatk = int(api_data["stats"][3]["base_stat"])
        spdef = int(api_data["stats"][4]["base_stat"])
        speed = int(api_data["stats"][5]["base_stat"])
        sprites = str(api_data["sprites"]["front_default"])
        return cls(pokemon_id, name, type1, type2, hp, atk, defense, spatk, spdef, speed, sprites)
    
    @classmethod
    def from_db_row(cls, row):
        """Create a Pokemon object from database row"""
        pokemon_id, name, type1, type2, hp, atk, defense, spatk, spdef, speed, sprites = row
        return cls(pokemon_id, name, type1, type2, hp, atk, defense, spatk, spdef, speed, sprites)
    
    def to_db_tuple(self):
        """Convert Pokemon to database tuple format"""
        return (self.id, self.name, self.type1, self.type2, self.hp, self.atk, self.defense, self.spatk, self.spdef, self.speed, self.sprites)
    
    def get_formatted_details(self):
        """Get formatted string of Pokemon details"""
        details = f"ID: {self.id}\n"
        details += f"Name: {self.name.capitalize()}\n\n"
        
        details += "Types:\n"
        details += f"  • {self.type1.capitalize()}\n"
        if self.type2:
            details += f"  • {self.type2.capitalize()}\n"
        details += "\n"
        
        details += "Stats:\n"
        details += f"  HP: {self.hp}\n"
        details += f"  Attack: {self.atk}\n"
        details += f"  Defense: {self.defense}\n"
        details += f"  Sp. Attack: {self.spatk}\n"
        details += f"  Sp. Defense: {self.spdef}\n"
        details += f"  Speed: {self.speed}\n"
        
        return details
    
    def get_sprite_url(self):
        """Get the front default sprite URL"""
        return self.sprites if self.sprites else None
