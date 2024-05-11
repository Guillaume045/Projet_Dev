import requests
import csv
import time
import os

esp32_ip = '192.168.4.1'  # Remplacez par l'adresse IP réelle de votre ESP32

url_temperature = 'http://' + esp32_ip + '/temperature'
url_humidite = 'http://' + esp32_ip + '/humidity'
url_luminosite = 'http://' + esp32_ip + '/luminosite'
url_led_on = 'http://' + esp32_ip + '/led/on'
url_led_off = 'http://' + esp32_ip + '/led/off'
url_servo_on = 'http://' + esp32_ip + '/servo/on'
url_servo_off = 'http://' + esp32_ip + '/servo/off'

response_temperature = requests.get(url_temperature)
response_humidite = requests.get(url_humidite)
response_luminosite = requests.get(url_luminosite)
response_led_on = requests.get(url_led_on)
time.sleep(2)
response_led_off = requests.get(url_led_off)
response_servo_on = requests.get(url_servo_on)
time.sleep(2)
response_servo_off = requests.get(url_servo_off)

# Fonction pour vérifier l'existence du dossier DB et le créer si nécessaire
def creer_dossier_db():
    if not os.path.exists('Serveur/DB'):
        os.makedirs('Serveur/DB')

# Appel de la fonction pour créer le dossier DB
creer_dossier_db()

# Fonction pour enregistrer les données dans un fichier CSV
def enregistrer_donnees(nom_fichier, date, heure, valeur):
    with open(os.path.join('Serveur/DB', nom_fichier), 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([date, heure, valeur])

# Fonction pour vérifier et écrire les en-têtes des fichiers CSV
def verifier_fichier(nom_fichier, entetes):
    try:
        with open(os.path.join('Serveur/DB', nom_fichier), 'r') as csvfile:
            pass  # Le fichier existe déjà
    except FileNotFoundError:
        with open(os.path.join('Serveur/DB', nom_fichier), 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(entetes)

# Les en-têtes des fichiers CSV
entetes_temperature = ['Date', 'Heure', 'Temperature']
entetes_humidite = ['Date', 'Heure', 'Humidite']
entetes_luminosite = ['Date', 'Heure', 'Luminosite']

# Vérification et écriture des en-têtes
verifier_fichier('temperature.csv', entetes_temperature)
verifier_fichier('humidite.csv', entetes_humidite)
verifier_fichier('luminosite.csv', entetes_luminosite)

# Récupération de la date et de l'heure actuelles
maintenant = time.localtime()
date_heure = time.strftime("%d-%m-%Y,%H:%M:%S", maintenant)
date, heure = date_heure.split(',')

# Pour la température
if response_temperature.status_code == 200:
    temperature = response_temperature.text
    print("Température récupérée:", temperature)  # Ajout de cette ligne pour le débogage
    enregistrer_donnees('temperature.csv', date, heure, temperature)
else:
    print("Erreur lors de la récupération de la température:", response_temperature.status_code)
    temperature = None
    enregistrer_donnees('temperature.csv', date, heure, temperature)

# Pour l'humidité
if response_humidite.status_code == 200:
    humidite = response_humidite.text
    print("Humidité récupérée:", humidite)  # Ajout de cette ligne pour le débogage
    enregistrer_donnees('humidite.csv', date, heure, humidite)
else:
    print("Erreur lors de la récupération de l'humidité:", response_humidite.status_code)
    humidite = None
    enregistrer_donnees('humidite.csv', date, heure, humidite)

# Pour la luminosité
if response_luminosite.status_code == 200:
    luminosite = response_luminosite.text
    enregistrer_donnees('luminosite.csv', date, heure, luminosite)

# Affichage : c'est pas utilise pour le code mais utilise pour les erreur si il y en as 
if response_led_on.status_code == 200:
    print("led: on")
else:
    print("Erreur lors de la récupération de l'led:", response_led_on.status_code)

if response_led_off.status_code == 200:
    print("led: off")
else:
    print("Erreur lors de la récupération de l'led:", response_led_off.status_code)
