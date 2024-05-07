import pywifi
import network
import time
from flask import Flask, request
import csv

# Définir le nom du réseau WiFi et le mot de passe
nom_wifi = "Mon réseau chelou"
mot_de_passe = ""

def connect_to_wifi(ssid, password):
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]

    # Supprimer toutes les connexions WiFi existantes
    #iface.disconnect()

    # Se connecter au réseau WiFi
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(ssid, password)

    while not sta_if.isconnected():
        pass

    print("Connecté au réseau WiFi")

    # Supprimer toutes les connexions WiFi existantes
    iface.disconnect()

    # Création de l'objet de configuration
    profile = pywifi.Profile()
    profile.ssid = ssid  # Nom du réseau WiFi
    profile.auth = pywifi.const.AUTH_ALG_OPEN  # Type d'authentification
    profile.akm.append(pywifi.const.AKM_TYPE_WPA2PSK)  # Type de cryptage
    profile.cipher = pywifi.const.CIPHER_TYPE_CCMP  # Algorithme de chiffrement
    profile.key = password  # Mot de passe

    # Ajouter le profil
    iface.remove_all_network_profiles()
    tmp_profile = iface.add_network_profile(profile)

    # Connexion au réseau WiFi
    iface.connect(tmp_profile)
    time.sleep(5)  # Attendre quelques secondes pour que la connexion soit établie

    # Vérifier si la connexion est établie
    if iface.status() == pywifi.const.IFACE_CONNECTED:
        print("Connecté au réseau WiFi avec succès.")
    else:
        print("Échec de la connexion au réseau WiFi.")

app = Flask(__name__)

def save_to_csv(data):
    with open('data.csv', 'a', newline='') as csvfile:
        fieldnames = ['temperature', 'humidity', 'luminosity']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Écrire les en-têtes du fichier CSV s'il est vide
        if csvfile.tell() == 0:
            writer.writeheader()

        # Écrire les données dans le fichier CSV
        writer.writerow(data)

@app.route('/endpoint', methods=['POST'])
def receive_data():
    data = request.json
    temperature = data.get('temperature')
    humidity = data.get('humidity')
    luminosity = data.get('luminosity')
    print("Données reçues - Température:", temperature, "°C | Humidité:", humidity, "% | Luminosité:", luminosity)

    # Enregistrer les données dans un fichier CSV
    save_to_csv(data)

    return "Données reçues avec succès et enregistrées dans le fichier CSV."

if __name__ == '__main__':
    connect_to_wifi(nom_wifi, mot_de_passe)  # Se connecter au réseau WiFi
    app.run(host='0.0.0.0', port=8080)  # Écoute sur toutes les interfaces sur le port 8080
