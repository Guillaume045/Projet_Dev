import time
import dht
import network
import socket
import esp
import os
import uos
import utime
import _thread as thread
from machine import Pin, PWM, ADC
esp.osdebug(None)

# Configuration du capteur DHT22
dht_pin = 4
dht_sensor = dht.DHT22(Pin(dht_pin))

# Configuration de la LED
led_pin = 2
led = Pin(led_pin, Pin.OUT)

# Configuration du servo-moteur
servo_pin = 14
servo_pwm = PWM(Pin(servo_pin), freq=50)

# Configuration du capteur de luminosité (photorésistance)
light_pin = 34
light_adc = ADC(Pin(light_pin))
light_adc.atten(ADC.ATTN_11DB)

# Configuration du point d'accès WiFi
ssid = 'Mon réseau chelou'
password = ''

# Création du dossier "DB" s'il n'existe pas déjà
if not 'DB' in uos.listdir('/'):
    uos.mkdir('/DB')

# Fonction pour lire la température et l'humidité
def read_temperature_humidity():
    try:
        dht_sensor.measure()
        temperature = dht_sensor.temperature()
        humidity = dht_sensor.humidity()
        return temperature, humidity
    except OSError as e:
        print("Erreur lors de la lecture du capteur DHT22:", e)
        return None, None

# Fonction pour lire l'intensité lumineuse
def read_light_intensity():
    light_value = light_adc.read()
    #print("Valeur de la luminosité:", light_value)
    return light_value

# Fonction pour contrôler la LED
def control_led(state):
    led.value(state)

# Fonction pour contrôler le servo-moteur
def control_servo_motor(angle):
    servo_pwm.duty(angle)

# Fonction pour mapper une valeur
def map_value(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

# Configuration du WiFi en point d'accès
def setup_wifi():        
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=ssid, password=password)
    print('Point d\'accès WiFi créé avec succès')
    print(ap.ifconfig())

# Fonction pour allumer la LED
def turn_on_led():
    led.on()

# Fonction pour éteindre la LED
def turn_off_led():
    led.off()

html_file_path = '/templates/index.html'

# Fonction pour gérer les requêtes HTTP
def http_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 80))
    sock.listen(5)
    print("Serveur HTTP démarré.")
    while True:
        client, addr = sock.accept()
        print('Nouvelle connexion depuis:', addr)
        request = client.recv(1024)
        request = str(request)
        #print("Requête reçue:", request)
        
        # page 
        if 'GET /index' in request:
            print("Requête pour la page home.")
            temperature = dht_sensor.temperature()
            humidity = dht_sensor.humidity()
            light_intensity = read_light_intensity()
            data = {'temperature': temperature, 'humidity': humidity, 'light_intensity': light_intensity}
            # Lisez le contenu de la page HTML
            with open(html_file_path, 'r') as f:
                html_content = f.read()
            # Remplacez les balises de données dans le HTML avec les valeurs actuelles
            html_content = html_content.replace('{temperature}', str(temperature))
            html_content = html_content.replace('{humidity}', str(humidity))
            html_content = html_content.replace('{light_intensity}', str(light_intensity))
            response = html_content
        elif 'GET /login' in request:
            print("Requête pour la page login.")
            with open('/templates/login.html', 'r') as f:
                response = f.read()
        elif 'GET /register' in request:
            print("Requête pour la page register.")
            with open('/templates/register.html', 'r') as f:
                response = f.read()
        elif 'GET /user' in request:
            print("Requête pour la page register.")
            with open('/templates/user.html', 'r') as f:
                response = f.read()
                
        # Fonction
        elif 'GET /led/on' in request:
            print("Requête pour allumer la LED.")
            turn_on_led()
            response = 'LED turned ON successfully'
        elif 'GET /led/off' in request:
            print("Requête pour éteindre la LED.")
            turn_off_led()
            response = 'LED turned OFF successfully'
        elif 'GET /servo/on' in request:
            print("Requête pour déplacer le servo à 40 degrés.")
            control_servo_motor(40)
            response = 'Servo moved to 40 degrees'
        elif 'GET /servo/off' in request:
            print("Requête pour déplacer le servo à 100 degrés.")
            control_servo_motor(100)
            response = 'Servo moved to 100 degrees'
        else:
            print("Requête invalide.")
            response = 'Invalid request'
        
        client.send('HTTP/1.1 200 OK\n')
        client.send('Content-Type: text/html\n')
        client.send('Connection: close\n\n')
        client.sendall(response.encode())
        client.close()

# Fonction pour enregistrer les données dans un fichier CSV avec date et heure
def enregistrer_donnees(nom_fichier, valeur):
    maintenant = utime.localtime()
    date_heure = "{:02d}-{:02d}-{:04d},{:02d}:{:02d}:{:02d}".format(maintenant[2], maintenant[1], maintenant[0], maintenant[3], maintenant[4], maintenant[5])
    with open('/DB/' + nom_fichier, 'a') as f:
        f.write(date_heure + ',' + str(valeur) + '\n')

# Fonction principale
def main():
    setup_wifi()
    # Lancer le serveur HTTP dans un thread séparé
    thread.start_new_thread(http_server, ())
    print("Serveur HTTP démarré.")
    
    while True:
        dht_sensor.measure()
        temperature = dht_sensor.temperature()
        humidity = dht_sensor.humidity()
        #luminosité = light_adc.read()

        # Enregistrer
        enregistrer_donnees('temperature.csv', temperature)
        enregistrer_donnees('humidity.csv', humidity)
        #enregistrer_donnees('luminosité.csv', luminosité)

        utime.sleep(5)

if __name__ == "__main__":
    main()
