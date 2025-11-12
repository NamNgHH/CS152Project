import sqlite3
import requests
import json

# connection and cursor
connection = sqlite3.connect('pokemon_information.db')
cursor = connection.cursor()

part_url = "https://pokeapi.co/api/v2/"

cursor.execute("""CREATE TABLE IF NOT EXISTS pokemon (id INTEGER PRIMARY KEY, name TEXT, stats TEXT, type TEXT, sprites TEXT)""")

for i in range (1, 2):
    pokemon_url = part_url + "pokemon/" + str(i)
    response = requests.get(pokemon_url)
    if response.status_code == 200:
        pokemon_data = response.json()
        pokemon_id = int(pokemon_data["id"])
        pokemon_name = str(pokemon_data["name"])
        pokemon_stats = json.dumps(pokemon_data["stats"])
        pokemon_type = json.dumps(pokemon_data["types"])
        pokemon_sprites = json.dumps(pokemon_data["sprites"])
        cursor.execute("""INSERT OR REPLACE INTO pokemon (id , name, stats, type, sprites) VALUES (?, ?, ?, ?, ?)""",
        (pokemon_id, pokemon_name, pokemon_stats, pokemon_type, pokemon_sprites)) 
    else:
        print("Failed to retrieve: ", i)


connection.commit()
connection.close()