#include <WiFi.h>
#include <Arduino.h>
#include <ESPAsyncWebServer.h>
#include <SPIFFS.h>
#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>

const char *ssid = "Nom du point d'acces"; // Nom du point d'accès WiFi
const char *password = "Mot de passe"; // Mot de passe du point d'accès WiFi

const int led = 2;
const int capteurLuminosite = 34;
const int DHTPin = 4; // Broche du capteur DHT11
const int DHTType = DHT11;

DHT dht(DHTPin, DHTType);

AsyncWebServer server(80);

void setup()
{
  Serial.begin(115200);
  Serial.println("\n");

  pinMode(led, OUTPUT);
  digitalWrite(led, LOW);
  pinMode(capteurLuminosite, INPUT);

  if(!SPIFFS.begin())
  {
    Serial.println("Erreur SPIFFS...");
    return;
  }

  // Créer le point d'accès WiFi
  WiFi.softAP(ssid, password);
  Serial.println("Point d'acces WiFi cree!");

  IPAddress IP = WiFi.softAPIP();
  Serial.print("Adresse IP du point d'acces WiFi: ");
  Serial.println(IP);

  dht.begin();

  server.on("/lireLuminosite", HTTP_GET, [](AsyncWebServerRequest *request)
  {
    int val = analogRead(capteurLuminosite);
    String luminosite = String(val);
    request->send(200, "text/plain", luminosite);
  });

  server.on("/temperature", HTTP_GET, [](AsyncWebServerRequest *request)
  {
    delay(2000); // Attendre 2 secondes pour permettre au capteur de stabiliser la lecture
    float temp = dht.readTemperature();
    if (isnan(temp)) {
      request->send(500, "text/plain", "Erreur de lecture du capteur de température");
    } else {
      request->send(200, "text/plain", String(temp));
    }
  });

  server.on("/humidite", HTTP_GET, [](AsyncWebServerRequest *request)
  {
    delay(2000); // Attendre 2 secondes pour permettre au capteur de stabiliser la lecture
    float humidite = dht.readHumidity();
    if (isnan(humidite)) {
      request->send(500, "text/plain", "Erreur de lecture du capteur d'humidité");
    } else {
      request->send(200, "text/plain", String(humidite));
    }
  });

  server.on("/on", HTTP_GET, [](AsyncWebServerRequest *request)
  {
    digitalWrite(led, HIGH);
    request->send(200);
  });

  server.on("/off", HTTP_GET, [](AsyncWebServerRequest *request)
  {
    digitalWrite(led, LOW);
    request->send(200);
  });

  server.begin();
  Serial.println("Serveur actif!");
}

void loop()
{

}
