import sqlite3

conn = sqlite3.connect('C:\\Users\\qcass\\Cours+tp\\B2\\Projet_Dev\\credential.db')

cur = conn.cursor()

conn.execute('''CREATE TABLE IF NOT EXISTS cred (
                    id INTEGER PRIMARY KEY,
                    Email TEXT NOT NULL,
                    Password TEXT NOT NULL
                )''')

cur.close()
conn.close()