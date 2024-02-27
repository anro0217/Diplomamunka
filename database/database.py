import sqlite3

conn = sqlite3.connect('application.db')
c = conn.cursor()

# Felhasználói tábla frissítése az email oszloppal
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
''')

conn.commit()
conn.close()
