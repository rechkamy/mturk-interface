import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

with open('data.sql') as f2:
    connection.executescript(f2.read())

connection.commit()
connection.close()
