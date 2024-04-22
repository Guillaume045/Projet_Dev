from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Route pour la page de connexion
@app.route('/login')
def login():
    return render_template('login.html')


# Route pour gérer la soumission du formulaire de connexion
@app.route('/login', methods=['POST'])
def login_submit():
    email = request.form['email']
    password = request.form['password']
    
    conn = sqlite3.connect('C:\\Users\\qcass\\Cours+tp\\B2\\Projet_Dev\\Database\\credential.db')
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM cred WHERE Email=? AND Password=?", (email, password))
    user = cur.fetchone()
    
    cur.close()
    conn.close()
    
    if user:
        # Authentification réussie, redirigez vers une page de réussite ou effectuez d'autres actions
        return redirect(url_for('home'))
    else:
        error = 'Identifiants incorrects'
        # Authentification échouée, redirigez vers la page de connexion avec un message d'erreur
        return render_template('login.html', error='Identifiants incorrects')


@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    password = request.form['password']
    
    conn = sqlite3.connect('C:\\Users\\qcass\\Cours+tp\\B2\\Projet_Dev\\Database\\credential.db')
    cur = conn.cursor()
    
    cur.execute("INSERT INTO cred (Email, Password) VALUES (?, ?)", (email, password))
    conn.commit()
    
    cur.close()
    conn.close()
    
    # Redirigez vers la page de connexion après l'inscription réussie
    return redirect(url_for('login'))

@app.route('/home')
def home():
    return render_template('home.html')

# Route pour la page de succès après connexion
@app.route('/success')
def success():
    return render_template('home.html')
    

if __name__ == '__main__':
    app.run(debug=True)