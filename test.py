import sqlite3

connection = sqlite3.connect("pokemon_information.db")
cursor = connection.cursor()

cursor.execute("SELECT * FROM pokemon")
rows = cursor.fetchall()

for row in rows:
    print(row)

connection.close()