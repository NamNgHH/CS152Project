import sqlite3
import requests
import json

# connection and cursor
connection = sqlite3.connect('pokemon_information.db')
cursor = connection.cursor()

part_url = "https://pokeapi.co/api/v2/"

cursor.execute("""CREATE TABLE IF NOT EXISTS pokemon (id INTEGER PRIMARY KEY, name TEXT, type1 TEXT, type2 TEXT, hp INTEGER, atk INTEGER, def INTEGER, spatk INTEGER, spdef INTEGER, speed INTEGER, sprites TEXT)""")

for i in range (1, 21):
    pokemon_url = part_url + "pokemon/" + str(i)
    response = requests.get(pokemon_url)
    if response.status_code == 200:
        pokemon_data = response.json()
        pokemon_id = int(pokemon_data["id"])
        pokemon_name = str(pokemon_data["name"])
        pokemon_type1 = str(pokemon_data["types"][0]["type"]["name"])
        if len(pokemon_data["types"]) > 1 :
            pokemon_type2 = str(pokemon_data["types"][1]["type"]["name"])
        else:
            pokemon_type2 = None
        pokemon_hp = int(pokemon_data["stats"][0]["base_stat"])
        pokemon_atk = int(pokemon_data["stats"][1]["base_stat"])
        pokemon_def = int(pokemon_data["stats"][2]["base_stat"])
        pokemon_spatk = int(pokemon_data["stats"][3]["base_stat"])
        pokemon_spdef = int(pokemon_data["stats"][4]["base_stat"])
        pokemon_speed = int(pokemon_data["stats"][5]["base_stat"])
        pokemon_sprites = str(pokemon_data["sprites"]["front_default"])
        cursor.execute("""INSERT OR REPLACE INTO pokemon (id , name, type1, type2, hp, atk, def, spatk, spdef, speed, sprites) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (pokemon_id, pokemon_name, pokemon_type1, pokemon_type2, pokemon_hp, pokemon_atk, pokemon_def, pokemon_spatk, pokemon_spdef, pokemon_speed, pokemon_sprites))
connection.commit()


cursor.execute("""CREATE TABLE IF NOT EXISTS item (id INTEGER PRIMARY KEY, name TEXT, effect TEXT, sprites TEXT)""")
for i in range (1,21):
    item_url = part_url + "item/" + str(i)
    response = requests.get(item_url)
    if response.status_code == 200:
        item_data = response.json()
        item_id = int(item_data["id"])
        item_name = str(item_data["name"])
        item_effect = str(item_data["effect_entries"][0]["effect"])
        item_sprite = str(item_data["sprites"]["default"])
        cursor.execute("""INSERT OR REPLACE INTO item (id, name, effect, sprites) VALUES (?, ?, ?, ?)""",
        (item_id, item_name, item_effect, item_sprite))
connection.commit()


cursor.execute("""CREATE TABLE IF NOT EXISTS move (id INTEGER PRIMARY KEY, name TEXT, accuracy INTEGER, power INTEGER, pp INTEGER, priority INTEGER, effect TEXT, class TEXT, type TEXT)""")
for i in range (1,21):
    move_url = part_url + "move/" + str(i)
    response = requests.get(move_url)
    if response.status_code == 200:
        move_data = response.json()
        move_id = int(move_data["id"])
        move_name = str(move_data["name"])
        move_accuracy = int(move_data["accuracy"]) if move_data["accuracy"] is not None else 0
        move_power = int(move_data["power"]) if move_data["power"] is not None else 0
        move_pp = int(move_data["pp"]) if move_data["pp"] is not None else 0
        move_priority = int(move_data["priority"]) if move_data["priority"] is not None else 0
        move_effect = str(move_data["effect_entries"][0]["effect"])
        move_class = str(move_data["damage_class"]["name"])
        move_type = str(move_data["type"]["name"])
        cursor.execute("""INSERT OR REPLACE INTO move (id , name, accuracy, power, pp, priority, effect, class, type) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (move_id, move_name, move_accuracy, move_power, move_pp, move_priority, move_effect, move_class, move_type))

connection.commit()
connection.close()