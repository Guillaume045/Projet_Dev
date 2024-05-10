import requests
import time

esp32_ip = '192.168.4.1'  # Remplacez par l'adresse IP réelle de votre ESP32

url_temperature = 'http://' + esp32_ip + '/temperature'
url_humidite = 'http://' + esp32_ip + '/humidite'
url_luminosite = 'http://' + esp32_ip + '/lireLuminosite'
url_led_on = 'http://' + esp32_ip + '/on'
url_led_off = 'http://' + esp32_ip + '/off'

response_temperature = requests.get(url_temperature)
response_humidite = requests.get(url_humidite)
response_luminosite = requests.get(url_luminosite)
response_led_on = requests.get(url_led_on)
time.sleep(2)
response_led_off = requests.get(url_led_off)

# Affichage : c'est pas utilise pour le code mais utilise pour les erreur si il y en as 
if response_temperature.status_code == 200:
    print("Température:", response_temperature.text)
else:
    print("Erreur lors de la récupération de la température:", response_temperature.status_code)

if response_humidite.status_code == 200:
    print("Humidité:", response_humidite.text)
else:
    print("Erreur lors de la récupération de l'humidité:", response_humidite.status_code)

if response_luminosite.status_code == 200:
    print("Luminosité:", response_luminosite.text)
else:
    print("Erreur lors de la récupération de la luminosité:", response_luminosite.status_code)

if response_led_on.status_code == 200:
    print("led: on")
else:
    print("Erreur lors de la récupération de l'led:", response_led_on.status_code)

if response_led_off.status_code == 200:
    print("led: off")
else:
    print("Erreur lors de la récupération de l'led:", response_led_off.status_code)
