import sqlite3

connection = sqlite3.connect("pokemon_information.db")
cursor = connection.cursor()

cursor.execute("SELECT * FROM pokemon")
pokemon_rows = cursor.fetchall()

for row in pokemon_rows:
    print(row[1])

cursor.execute("SELECT * FROM item")
item_rows = cursor.fetchall()

for row in item_rows:
    print(row[1])

cursor.execute("SELECT * FROM move")
move_rows = cursor.fetchall()

for row in move_rows:
    print(row[1])
connection.close()