import requests
import csv
import time
import os

# IP de la connection pour faire les requêtes
ip = '192.168.4.1'
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

# Fait la requête à la page html
response_temperature = requests.get(url_temperature)
response_humidite = requests.get(url_humidite)
response_luminosite = requests.get(url_luminosite)

# Fonction pour vérifier l'existence du dossier DB et le créer si nécessaire
def creer_dossier_db():
    if not os.path.exists('Serveur/DB'):
        os.makedirs('Serveur/DB')

# Fonction pour enregistrer les données dans un fichier CSV
def enregistrer_donnees(nom_fichier, date, heure, valeur):
    with open(os.path.join('Serveur/DB', nom_fichier), 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([date, heure, valeur])

# Fonction pour vérifier et écrire les en-têtes des fichiers CSV
def verifier_fichier(nom_fichier, entetes):
    try:
        with open(os.path.join('Serveur/DB', nom_fichier), 'r') as csvfile:
            pass
    except FileNotFoundError:
        with open(os.path.join('Serveur/DB', nom_fichier), 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(entetes)

if __name__ == "__main__":
    creer_dossier_db()
    verifier_fichier('temperature.csv', entetes_temperature)
    verifier_fichier('humidite.csv', entetes_humidite)
    verifier_fichier('luminosite.csv', entetes_luminosite)

    # Pour la température
    if response_temperature.status_code == 200:
        temperature = response_temperature.text
        print("Temperature recuperee:", temperature)
        enregistrer_donnees('temperature.csv', date, heure, temperature)
    else:
        print("Erreur lors de la recuperation de la temperature:", response_temperature.status_code)
        temperature = None
        enregistrer_donnees('temperature.csv', date, heure, temperature)

    # Pour l'humidité
    if response_humidite.status_code == 200:
        humidite = response_humidite.text
        print("Humidite recuperee:", humidite)
        enregistrer_donnees('humidite.csv', date, heure, humidite)
    else:
        print("Erreur lors de la recuperation de l humidite:", response_humidite.status_code)
        humidite = None
        enregistrer_donnees('humidite.csv', date, heure, humidite)

    # Pour la luminosité
    if response_luminosite.status_code == 200:
        luminosite = response_luminosite.text
        print("luminosite recuperee:", luminosite)
        enregistrer_donnees('luminosite.csv', date, heure, luminosite)
    else:
        print("Erreur lors de la recuperation de la luminosite:", response_luminosite.status_code)
        luminosite = None
        enregistrer_donnees('luminosite.csv', date, heure, humidite)
