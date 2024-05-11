from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
import pandas as pd

app = Flask(__name__)

# Chemin du répertoire 
template_dir = os.path.abspath('Serveur/Template')
static_dir = os.path.abspath('Serveur/Styles')

# Définition du répertoire des templates et des fichiers statiques
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

# Route pour la page de connexion
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
    
    conn = sqlite3.connect('Serveur/Database/credential.db')
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
    # Lire le fichier CSV
    df = pd.read_csv('Serveur/DB/temperature.csv')
    # Obtenir la dernière valeur de la dernière colonne
    last_value = df.iloc[-1, -1]
    print(last_value)
    return render_template('index.html', temperature=last_value)

if __name__ == '__main__':
    app.run(debug=True)
