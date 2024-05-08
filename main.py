from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Chemin du répertoire des templates
template_dir = os.path.abspath('Template')

# Chemin du répertoire des fichiers statiques (CSS, JavaScript, images, etc.)
static_dir = os.path.abspath('Styles')

# Définition du répertoire des templates et des fichiers statiques
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

# Adresse IP de votre ESP32
esp32_ip = '192.168.4.1'  # Remplacez par l'adresse IP réelle de votre ESP32

# Route pour la page d'accueil
@app.route('/index')
def home():
    # URL du serveur HTTP sur ESP32 pour obtenir les données de température et d'humidité
    url = 'http://' + esp32_ip + '/temperature'
    # Effectuer la requête GET
    response = requests.get(url)
    # Vérifier si la requête a réussi
    if response.status_code == 200:
        temperature_data = response.json()  # Si la réponse est JSON
        # Vous pouvez également utiliser response.text si les données ne sont pas au format JSON
        return render_template('index.html', temperature=temperature_data['temperature'], humidity=temperature_data['humidity'])
    else:
        error_message = "Erreur lors de la récupération des données depuis l'ESP32."
        return render_template('index.html', error=error_message)

# Route pour la page de connexion
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = sqlite3.connect('Database/credential.db')
        cur = conn.cursor()
        
        cur.execute("SELECT * FROM cred WHERE Email=? AND Password=?", (email, password))
        user = cur.fetchone()
        
        cur.close()
        conn.close()
        
        if user:
            # Authentification réussie, redirigez vers une page de réussite ou effectuez d'autres actions
            return redirect(url_for('success'))
        else:
            error = 'Identifiants incorrects'
            # Authentification échouée, redirigez vers la page de connexion avec un message d'erreur
            return render_template('login.html', error='Identifiants incorrects')
    else:
        # Si la méthode de requête n'est pas POST, affichez simplement la page de connexion
        return render_template('login.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    password = request.form['password']
    
    conn = sqlite3.connect('Database/credential.db')
    cur = conn.cursor()
    
    cur.execute("INSERT INTO cred (Email, Password) VALUES (?, ?)", (email, password))
    conn.commit()
    
    cur.close()
    conn.close()
    
    # Redirigez vers la page de connexion après l'inscription réussie
    return redirect(url_for('login'))

# Route pour la page de succès après connexion
@app.route('/success')
def success():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
