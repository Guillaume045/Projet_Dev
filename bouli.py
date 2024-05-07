import requests

# Adresse IP de votre ESP32
esp32_ip = '192.168.4.1'  # Remplacez par l'adresse IP réelle de votre ESP32

# URL du serveur HTTP sur ESP32 pour obtenir les données de température et d'humidité
url = 'http://' + esp32_ip + '/temperature'

# Effectuer la requête GET
response = requests.get(url)

# Vérifier si la requête a réussi
if response.status_code == 200:
    print("Données de température et d'humidité reçues avec succès:")
    print(response.text)
else:
    print("Erreur lors de la récupération des données:", response.status_code)
