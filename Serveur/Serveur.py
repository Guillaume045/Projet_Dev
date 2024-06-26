# Code permetant de géré les page html et de relier la db au site 
# Créer le 9/04/2024

from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
import pandas as pd

app = Flask(__name__)

# Chemin du répertoire 
template_dir = os.path.abspath('Serveur/Template')
static_dir = os.path.abspath('Serveur/Styles')
# Répertoire des templates et des fichiers statiques
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect('Serveur/Database/credential.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM cred WHERE Email=? AND Password=?", (email, password))
        user = cur.fetchone()
        cur.close()
        conn.close()
        
        if user:    # Authentification réussie
            return redirect(url_for('success'))
        else:       # Authentification échouée
            error = 'Identifiants incorrects'
            return render_template('login.html', error='Identifiants incorrects')
    else:
        return render_template('login.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    password = request.form['password']
    conn = sqlite3.connect('Serveur/Database/credential.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO cred (Email, Password) VALUES (?, ?)", (email, password))
    conn.commit()
    cur.close()
    conn.close()
    
    return redirect(url_for('login'))

@app.route('/success')
def success():
    # Lire les fichiers CSV
    df_temperature = pd.read_csv('Serveur/Database/temperature.csv')
    df_humidite = pd.read_csv('Serveur/Database/humidite.csv')
    df_luminosite = pd.read_csv('Serveur/Database/luminosite.csv')
    df_prediction_temperature = pd.read_csv('Serveur/Database/prediction_temperature.csv')
    df_prediction_humidite = pd.read_csv('Serveur/Database/prediction_humidite.csv')
    df_prediction_luminosite = pd.read_csv('Serveur/Database/prediction_luminosite.csv')
    # Obtenir la dernière valeur de la dernière colonne
    value_temperature = df_temperature.iloc[-1, -1]
    value_humidite = df_humidite.iloc[-1, -1]
    value_luminosite = df_luminosite.iloc[-1, -1]
    value_prediction_temperature = df_prediction_temperature.iloc[-1, -1]
    value_prediction_humidite = df_prediction_humidite.iloc[-1, -1]
    value_prediction_luminosite = df_prediction_luminosite.iloc[-1, -1]
    return render_template('index.html', temperature=value_temperature, humidite=value_humidite, luminosite=value_luminosite, prediction_temperature=value_prediction_temperature, prediction_humidite=value_prediction_humidite, prediction_luminosite=value_prediction_luminosite)

@app.route('/user')
def user():
    return render_template('user.html')

if __name__ == '__main__':
    app.run(debug=True)
