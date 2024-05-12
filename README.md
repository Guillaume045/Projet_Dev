# Projet_Dev Serre connecté

## I.Introduction 

Bienvenue dans notre projet de serre connectée ! Notre objectif est de créer un système de serre connecté pour simplifier l'utilisateur dans sont cotidient et de ne pas être tout le temps entrain de s'occuper de sa serre.

Notre serre sera équipée de capteurs pour mesurer l'humidité, la température et la luminosité à l'intérieur de la serre. Ces données seront transmises et affichées sur un site web, nous permettant de surveiller les conditions et de procéder aux ajustements nécessaires.

Pour garantir les bonnes conditions, notre serre comportera également des actionneurs capables d'ouvrir et de fermer la serre, ainsi que des LED pour éclairé si besoin.

--- 

Le Projet est coupé en deux partie c'est pour sela que vous pourrier voir deux dossier principal dans le projet.
- Une partie sur IOT de notre carte ESP32 qui viens a récupére les valeur.
- Une autre partie serveur qui viens géré la récupération des valeur et le site web.

---

## Sommaire
- I.Introduction
- II. Conception de serre
- III. Langage utilisé
- IV. Capteurs & actionneurs
- V. Câblage & consommation d'énergie
- VI. Base de données & stockage de données
- VII. Site Web & interface utilisateur
- VIII. Défis & solutions
- IX. Conclusion

## II.Conception de serre
La conception de notre serre connectée a été pensée pour être fonctionnelle et efficace. Nous avons choisi un design compact et modulaire pour faciliter l'installation et la maintenance. 
![Serre](/Serveur/Images/serre.png)

## III. Langage utilisé
Nous sommes tout d'abord partis pour faire ce projet en utilisant le logiciel [PlatformIO](https://platformio.org/) car nous souhaitons découvrir cet IDE qui est une extension présente dans VSCode, 
![image10](/Serveur/Images/platformio.svg)
![image12](/Serveur/Images/C++.png)
mais nous avons rencontré des problèmes dans la réalisation de fichier pour avoir une basse de données donc nous nous sommes replié sur la deuxième option qui était de le faire en MicroPython avec [Thonny](https://thonny.org/). 
![image13](/Serveur/Images/thonny.png)
![image14](/Serveur/Images/micropython.png)

## IV. Capteurs & actionneurs

### Capteurs
Nous utilisons les capteurs suivants pour mesurer la température, la luminosité et la teneure en humidité à l’intérieur de la serre :

#### Capteur de température et d'humidité DHT11
Le DHT11 est un capteur de température et d'humidité.
![image2](/Serveur/Images/DHT11.jpg)
Lien pour plus d'information : https://components101.com/sensors/dht11-temperature-sensor

#### Capteur luminosité Photorésistance 
Une photorésistance est un composant électronique dont la résistivité varie en fonction de la quantité de lumière incidente : plus elle est éclairée, plus sa résistivité baisse.
![image3](/Serveur/Images/Capteur-De-Lumiere-LDR-5-mm-Photoresistance-Best-buy-tunisie-prix-tunisie.webp)
Lien pour plus d'information : https://www.electricity-magnetism.org/fr/photoresistance-ldr/

### Actionneurs
Nous utilisons les actionneurs suivants pour contrôler la serre connecté :

#### Servomoteur sg90
Un servomoteur, c'est un type de moteur qui peut être contrôlé avec précision pour se déplacer vers une position spécifique. Nous l'utilisons pour contrôler le système d'ouverture et de fermeture de la serre.
![image4](/Serveur/Images/servomotor-sg90.jpg)
Lien pour plus d'information : https://www.friendlywire.com/projects/ne555-servo-safe/SG90-datasheet.pdf

#### Led
Nous utilisons aussi des LED pour éclairer la serre si nécessaire, nous permettant de simuler des conditions de luminosité différentes pour les plantes.
![image2](/Serveur/Images/Light-Emitting-Diode-LED.png)

## V. Câblage & consommation d'énergie

ESP32 WROOM DevKit générique:
![image1](/Serveur/Images/doc-esp32-pinout-reference-wroom-devkit.webp)

Récapitulatif de tous les pins GPIO de l’ESP32:

| GPIO | INPUT | OUTPUT
|:-:   |:-:    |:-:
|0|OUI (Pullup interne)|OUI
|1 (TX0)|NON|OUI
|2|OUI (Pulldown interne)|OUI
|3 (RX0)|OUI|NON
|4|OUI|OUI
|5|OUI|OUI
|6|NON|NON
|7|NON|NON
|8|NON|NON
|9|NON|NON
|10|NON|NON
|11|NON|NON
|12 (MTDI)|OUI (Pulldown interne)|OUI
|13|OUI|OUI
|14|OUI|OUI
|15 (MTDO)|OUI (Pullup interne)|OUI
|16|OUI|OUI
|17|OUI|OUI
|18|OUI|OUI
|19|OUI|OUI
|21|OUI|OUI
|22|OUI|OUI
|23|OUI|OUI
|25|OUI|OUI
|26|OUI|OUI
|27|OUI|OUI
|32|OUI|OUI
|33|OUI|OUI
|34|OUI|NON
|35|OUI|NON
|36 (VP)|OUI|NON
|39 (VN)|OUI|NON
|EN|NON|NON

## VI. Base de données & stockage de données
Pour stocker les données collectées par les capteurs, nous avons choisi d'utiliser une base de données CSV. Cette solution simple et efficace nous permet de stocker les données de manière organisée et facilement accessible.

## VII. Site Web & interface utilisateur
Pour visualiser les données collectées par les capteurs et contrôler les actionneurs, nous avons créé un site web avec une interface utilisateur intuitive. Le site web est accessible depuis n'importe quel navigateur web et sur n'importe qu'elle plateforme (téléphone, tablette, ordinateur), permet à l'utilisateur de surveiller les conditions de la serre en temps réel.

## VIII. Défis & solutions
1. Base de données : La carte utilisée ne prend pas en charge l'utilisation de bases de données. Par conséquent, une alternative consiste à recourir à l'utilisation de fichiers au format .csv pour le stockage des données.
2. Capteur de luminosité : Malheureusement, le capteur de luminosité ne fonctionne pas comme prévu lorsqu'il est utilisé avec MicroPython. Cette anomalie nécessite une révision de l'implémentation ou l'exploration d'autres langages de programmation comme le C++ pour obtenir un fonctionnement optimal.
3. Affichage d'images : L'environnement de développement Thonny pour MicroPython ne prend pas en charge l'affichage d'images. Pour contourner cette limitation, nous avons créer des icônes à l'aide d'HTML, une autre solution aurait été de changer de langage pour utiliser un langage qui prend en charge l'utilisation d'image.
4. Communication Serveur-Client : En raison de difficultés rencontrées avec la connexion à Ynov, l'établissement d'un serveur dédié s'est avéré impossible. En conséquence, nous avons entrepris de transformer le client en serveur. Toutefois, nous sommes toujours en train de résoudre ce problème en utilisant notre ordinateur personnel comme serveur de secours. Nous avons essayer avec deux cartes, cependant dû a des problèmes de communication nous avons abandonné cette idée.
5. Stockage des Données : Actuellement, aucune solution de stockage ne satisfait pleinement les besoins du projet. La carte n'ayant pas assez de mémoire nous recherchons des solutions alternatives qui pourrait-être par exemple changer les librairies utilisés.

## IX. Conclusion

Ce projet de serre connectée nous a permis de développer et renforcer certaines compétences.

L'utilisation de technologies telles que le langage de programmation C++ et MicroPython, ainsi que des plates-formes comme PlatformIO et Thonny, ont permis de développer une architecture logicielle robuste et adaptable. Malgré les défis rencontrés, tels que l'absence de données avec certaines fonctionnalités ou la nécessité d'ajuster le langage de programmation en cours de route, nous avons su trouver des solutions pour surmonter ces obstacles et garantir le bon fonctionnement du système.

La gestion des données a également été un aspect crucial de ce projet. En choisissant une base de données CSV pour stocker les informations collectées par les capteurs, nous avons privilégié une approche plus simple et efficace, tout en étant adaptée aux besoins de notre application.

Enfin, le développement d'une interface utilisateur simple et accessible via un site web a permet aux utilisateurs de surveiller et de contrôler la serre à distance, offrant ainsi un certain niveau de commodité et de flexibilité.