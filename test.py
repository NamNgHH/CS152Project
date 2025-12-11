import sqlite3

connection = sqlite3.connect("pokemon_information.db")
cursor = connection.cursor()

cursor.execute("SELECT * FROM pokemon")
pokemon_rows = cursor.fetchall()

for row in pokemon_rows:
    print(row[13])

    