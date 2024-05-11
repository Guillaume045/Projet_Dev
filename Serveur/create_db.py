import sqlite3
import os

def Fonction_DB_LR():
    db_folder = 'Serveur/Database'
    db_file = os.path.join(db_folder, 'credential.db')

    # Vérifier le dossier existe ou créer le
    if not os.path.exists(db_folder):
        os.makedirs(db_folder)
        print("Dossier cree :", db_folder)
    else:
        print("Le dossier existe deja :", db_folder)

    # Vérifier le fichier de données existe
    if os.path.exists(db_file):
        print("Le fichier de base de donnees existe deja :", db_file)
    else:
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        conn.execute('''CREATE TABLE IF NOT EXISTS cred (
                            id INTEGER PRIMARY KEY,
                            Email TEXT NOT NULL,
                            Password TEXT NOT NULL
                        )''')

        cur.close()
        conn.close()

        print("Le fichier de base de donnees a ete cree avec succes :", db_file)

if __name__ == "__main__":
    Fonction_DB_LR()
