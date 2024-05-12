# Code pour collecter les donné se trouvant sur la carte esp32 via des requette HTML
# Créer le 8/05/2024

import requests
import csv
import time
import os

# IP de la connection pour faire les requêtes
ip = '192.168.4.1'

# Chemin du Dossier de sauvegarde
chemin = 'Serveur/Database'

# URL pour récupérer les valeurs
url_temperature = 'http://' + ip + '/temperature'
url_humidite = 'http://' + ip + '/humidity'
url_luminosite = 'http://' + ip + '/luminosite'

# Les en-têtes des fichiers CSV
entetes_temperature = ['Date', 'Heure', 'Temperature']
entetes_humidite = ['Date', 'Heure', 'Humidite']
entetes_luminosite = ['Date', 'Heure', 'Luminosite']

# Récupération de la date et de l'heure actuelles
maintenant = time.localtime()
date_heure = time.strftime("%d-%m-%Y,%H:%M:%S", maintenant)
date, heure = date_heure.split(',')

# Fonction pour faire une requête HTTP et enregistrer les données
def collecter_et_enregistrer(url, nom_fichier, entetes):
    response = requests.get(url)
    if response.status_code == 200:
        valeur = response.text
        print(f"Donnees recuperees depuis {url} :", valeur)
    else:
        print(f"Erreur lors de la recuperation des donnees depuis {url} :", response.status_code)
        valeur = None

    creer_dossier()
    verifier_fichier(nom_fichier, entetes)
    enregistrer_donnees(nom_fichier, date, heure, valeur)

# Fonction pour vérifier l'existence du dossier DB et le créer si nécessaire
def creer_dossier():
    if not os.path.exists(chemin):
        os.makedirs(chemin)

# Fonction pour vérifier et écrire les en-têtes des fichiers CSV
def verifier_fichier(nom_fichier, entetes):
    try:
        with open(os.path.join(chemin, nom_fichier), 'r') as csvfile:
            pass
    except FileNotFoundError:
        with open(os.path.join(chemin, nom_fichier), 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(entetes)

# Fonction pour enregistrer les données dans un fichier CSV
def enregistrer_donnees(nom_fichier, date, heure, valeur):
    with open(os.path.join(chemin, nom_fichier), 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([date, heure, valeur])

if __name__ == "__main__":
    collecter_et_enregistrer(url_temperature, 'temperature.csv', entetes_temperature)
    collecter_et_enregistrer(url_humidite, 'humidite.csv', entetes_humidite)
    collecter_et_enregistrer(url_luminosite, 'luminosite.csv', entetes_luminosite)
