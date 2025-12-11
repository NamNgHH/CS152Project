import sqlite3
import requests
import json

# connection and cursor
connection = sqlite3.connect('pokemon_information.db')
cursor = connection.cursor()

part_url = "https://pokeapi.co/api/v2/"

cursor.execute("PRAGMA table_info(pokemon)")
pokemon_columns = {col[1] for col in cursor.fetchall()}
for col in ("ability1", "ability2", "ability3"):
    if col not in pokemon_columns:
        cursor.execute(f"ALTER TABLE pokemon ADD COLUMN {col} TEXT")


cursor.execute("""CREATE TABLE IF NOT EXISTS pokemon (id INTEGER PRIMARY KEY, name TEXT, type1 TEXT, type2 TEXT, hp INTEGER, atk INTEGER, def INTEGER, spatk INTEGER, spdef INTEGER, speed INTEGER, sprites TEXT, ability1 TEXT, ability2 TEXT, ability3 TEXT)""")

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
        pokemon_ability1 = str(pokemon_data["abilities"][0]["ability"]["name"])
        if len(pokemon_data["abilities"]) > 1 :
            pokemon_ability2 = str(pokemon_data["abilities"][1]["ability"]["name"])
        else:
            pokemon_ability2 = None
        if len(pokemon_data["abilities"]) > 2 :
            pokemon_ability3= str(pokemon_data["abilities"][2]["ability"]["name"])
        else:
            pokemon_ability3 = None
        cursor.execute("""INSERT OR REPLACE INTO pokemon (id , name, type1, type2, hp, atk, def, spatk, spdef, speed, sprites, ability1, ability2, ability3) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (pokemon_id, pokemon_name, pokemon_type1, pokemon_type2, pokemon_hp, pokemon_atk, pokemon_def, pokemon_spatk, pokemon_spdef, pokemon_speed, pokemon_sprites, pokemon_ability1, pokemon_ability2, pokemon_ability3))
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
cursor.execute("""CREATE TABLE IF NOT EXISTS pokemon_moves (pokemon_id INTEGER, move_id INTEGER, PRIMARY KEY (pokemon_id, move_id), FOREIGN KEY (pokemon_id) REFERENCES pokemon(id), FOREIGN KEY (move_id) REFERENCES move(id))""")
print("Fetching Pokemon and their moves...")
fetched_moves = set()
for i in range (1, 21):
    pokemon_url = part_url + "pokemon/" + str(i)
    response = requests.get(pokemon_url)
    if response.status_code == 200:
        pokemon_data = response.json()
        pokemon_id = int(pokemon_data["id"])
        print(f"Processing Pokemon #{pokemon_id}: {pokemon_data['name']}")
        moves = pokemon_data.get("moves", [])
        print(f"  Found {len(moves)} moves")
        for move_entry in moves:
            move_url = move_entry["move"]["url"]
            move_name = move_entry["move"]["name"]
            move_id_from_url = int(move_url.split("/")[-2])
            if move_id_from_url not in fetched_moves:
                try:
                    move_response = requests.get(move_url)
                    if move_response.status_code == 200:
                        move_data = move_response.json()
                        move_id = int(move_data["id"])
                        move_accuracy = int(move_data["accuracy"]) if move_data["accuracy"] is not None else 0
                        move_power = int(move_data["power"]) if move_data["power"] is not None else 0
                        move_pp = int(move_data["pp"]) if move_data["pp"] is not None else 0
                        move_priority = int(move_data["priority"]) if move_data["priority"] is not None else 0
                        move_effect = ""
                        if move_data.get("effect_entries") and len(move_data["effect_entries"]) > 0:
                            move_effect = str(move_data["effect_entries"][0].get("effect", ""))
                        
                        move_class = str(move_data["damage_class"]["name"])
                        move_type = str(move_data["type"]["name"])
                        cursor.execute("""INSERT OR REPLACE INTO move (id, name, accuracy, power, pp, priority, effect, class, type) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (move_id, move_name, move_accuracy, move_power, move_pp, move_priority, move_effect, move_class, move_type))
                        fetched_moves.add(move_id)
                        print(f"    Saved move: {move_name} (ID: {move_id})")
                except Exception as e:
                    print(f"    Error fetching move {move_name}: {str(e)}")
                    continue
            try:
                cursor.execute("""INSERT OR IGNORE INTO pokemon_moves (pokemon_id, move_id) VALUES (?, ?)""",
                (pokemon_id, move_id_from_url))
            except Exception as e:
                print(f"    Error linking move {move_name} to Pokemon {pokemon_id}: {str(e)}")
        
        connection.commit()

print(f"\nCompleted! Fetched {len(fetched_moves)} unique moves.")

print("\nFetching additional moves (1-20)...")
for i in range (1, 21):
    if i not in fetched_moves:
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
            
            move_effect = ""
            if move_data.get("effect_entries") and len(move_data["effect_entries"]) > 0:
                move_effect = str(move_data["effect_entries"][0].get("effect", ""))
            
            move_class = str(move_data["damage_class"]["name"])
            move_type = str(move_data["type"]["name"])
            cursor.execute("""INSERT OR REPLACE INTO move (id, name, accuracy, power, pp, priority, effect, class, type) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (move_id, move_name, move_accuracy, move_power, move_pp, move_priority, move_effect, move_class, move_type))
            print(f"  Saved move: {move_name} (ID: {move_id})")

connection.commit()
connection.close()
print("\nAll done!")