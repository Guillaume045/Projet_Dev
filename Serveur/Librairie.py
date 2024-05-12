# Code qui télécharger les librairie n'ésaisaire pour le projet
# Créer le 12/05/2024

import subprocess

def installer_librairies():
    librairies = [
        "flask",
        "pandas",
        "statsmodels",
        "scikit-learn",
        "sqlite3",
        "requests",
        "schedule"
    ]

    for librairie in librairies:
        print(f"Installation de la librairie {librairie}...")
        subprocess.run(["pip", "install", librairie])

if __name__ == "__main__":
    installer_librairies()
