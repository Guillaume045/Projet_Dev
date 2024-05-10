import sqlite3

conn = sqlite3.connect('Database/credential.db')

cur = conn.cursor()

conn.execute('''CREATE TABLE IF NOT EXISTS cred (
                    id INTEGER PRIMARY KEY,
                    Email TEXT NOT NULL,
                    Password TEXT NOT NULL
                )''')

cur.close()
conn.close()

conn_temp = sqlite3.connect('Database/temperature.db')
cur_temp = conn_temp.cursor()

conn_temp.execute('''CREATE TABLE IF NOT EXISTS temperature (
                    id INTEGER PRIMARY KEY,
                    Date TEXT NOT NULL,
                    Temperature REAL NOT NULL
                )''')

cur_temp.close()
conn_temp.close()

conn_light = sqlite3.connect('Database/luminosite.db')
cur_light = conn_light.cursor()

conn_light.execute('''CREATE TABLE IF NOT EXISTS luminosite (
                    id INTEGER PRIMARY KEY,
                    Date TEXT NOT NULL,
                    Luminosite REAL NOT NULL
                )''')

cur_light.close()
conn_light.close()