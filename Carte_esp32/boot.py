import network
import socket
import dht
import machine
import time

# Configuration du point d'accès WiFi
ssid = 'Mon réseau chelou'
password = 'MotDePasse'

# Configuration du capteur DHT22
dht_pin = 4
dht_sensor = dht.DHT22(machine.Pin(dht_pin))

# Configuration de la photorésistance
light_pin = 34
light_adc = machine.ADC(machine.Pin(light_pin))

# Configuration de la LED
led_pin = 2
led = machine.Pin(led_pin, machine.Pin.OUT)

# Configuration du Servomoteur
servo_pin = 12
servo = machine.PWM(machine.Pin(servo_pin), freq=50)
servo_min = 40
servo_max = 100

# Configuration du serveur HTTP
server_address = ('', 80)

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
    return light_adc.read()

# Fonction pour allumer la LED
def turn_led_on():
    led.value(1)

# Fonction pour éteindre la LED
def turn_led_off():
    led.value(0)

# Fonction pour faire tourner le servomoteur à 40 degrés
def turn_servo_on():
    servo.duty(servo_min)

# Fonction pour faire tourner le servomoteur à 100 degrés
def turn_servo_off():
    servo.duty(servo_max)

# Fonction pour gérer les requêtes HTTP
def handle_http_request(client_socket):
    request_data = client_socket.recv(1024)
    request_text = request_data.decode('utf-8')
    if 'GET /temperature' in request_text:
        temperature, _ = read_temperature_humidity()
        if temperature is not None:
            response_body = '{:.1f}'.format(temperature)
        else:
            response_body = 'Failed to read temperature data.'
    elif 'GET /humidity' in request_text:
        _, humidity = read_temperature_humidity()
        if humidity is not None:
            response_body = '{:.1f}'.format(humidity)
        else:
            response_body = 'Failed to read humidity data.'
    elif 'GET /luminosite' in request_text:
        light_intensity = read_light_intensity()
        response_body = '{}'.format(light_intensity)
    elif 'GET /led/on' in request_text:
        turn_led_on()
        response_body = 'LED turned on'
    elif 'GET /led/off' in request_text:
        turn_led_off()
        response_body = 'LED turned off'
    elif 'GET /servo/on' in request_text:
        turn_servo_on()
        response_body = 'Servo turned to 40 degrees'
    elif 'GET /servo/off' in request_text:
        turn_servo_off()
        response_body = 'Servo turned to 100 degrees'
    else:
        response_body = 'Invalid request'
    response_headers = 'HTTP/1.1 200 OK\nContent-Type: text/plain\nContent-Length: {}\n\n'.format(len(response_body))
    response = response_headers + response_body
    client_socket.send(response.encode('utf-8'))
    client_socket.close()

# Configuration du WiFi en point d'accès
def setup_wifi():
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=ssid, password=password)
    print('Point d\'accès WiFi créé avec succès')
    print(ap.ifconfig())

def main():
    setup_wifi()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(server_address)
    server_socket.listen(5)
    print('Serveur HTTP démarré.')

    while True:
        client_socket, client_address = server_socket.accept()
        #print('Nouvelle connexion depuis:', client_address)
        handle_http_request(client_socket)

if __name__ == "__main__":
    main()