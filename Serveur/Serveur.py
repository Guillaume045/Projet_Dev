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
    df_temperature = pd.read_csv('Serveur/DB/temperature.csv')
    df_humidite = pd.read_csv('Serveur/DB/humidite.csv')
    df_luminosite = pd.read_csv('Serveur/DB/luminosite.csv')
    # Obtenir la dernière valeur de la dernière colonne
    value_temperature = df_temperature.iloc[-1, -1]
    value_humidite = df_humidite.iloc[-1, -1]
    value_luminosite = df_luminosite.iloc[-1, -1]
    #print(value_temperature)
    #print(value_humidite)
    #print(value_luminosite)
    return render_template('index.html', temperature=value_temperature, humidite=value_humidite, luminosite=value_luminosite)

@app.route('/prevision')
def prevision():
    return render_template('prevision.html')

@app.route('/user')
def user():
    return render_template('user.html')

if __name__ == '__main__':
    app.run(debug=True)
