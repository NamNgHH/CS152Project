import sqlite3

connection = sqlite3.connect("pokemon_information.db")
cursor = connection.cursor()

cursor.execute("SELECT sprite FROM pokemon WHERE id = ?", (1,))
rows = cursor.fetchall()
conn.close()
print(rows)