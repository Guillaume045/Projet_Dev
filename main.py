# Avoir un main pour lavé les programme en une seul fois
# Créer le 12/05/2024

import subprocess
import schedule
import time

def execute_collecte():
    process_collecte = subprocess.Popen("python Serveur/Collecte.py", shell=True)   # Lance le scipt Collecte
    process_collecte.communicate()  # Attend la fin de l'exécution du scipt Collecte
    subprocess.Popen("python Serveur/Prevision.py", shell=True) # Lance le scipt Prevision

if __name__ == "__main__":
    commandes = [
        "python Serveur/Create_db.py",
        "python Serveur/Serveur.py",
    ]

    for commande in commandes:
        subprocess.Popen(commande, shell=True)

    # Planifier l'exécution de Collecte.py toutes les minutes
    schedule.every().minute.do(execute_collecte)

    while True:
        schedule.run_pending()
        time.sleep(0.5)
