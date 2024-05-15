from flask import Flask, render_template, request, redirect, url_for, session
import secrets
import sqlite3

# Session key generated randomly
secrets_key = secrets.token_hex(16)
app = Flask(__name__)
app.secret_key = secrets_key

#route for page of index
@app.route('/')
def index():
    return render_template('index.html')

#route for page of login
@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    try:
        #
        username = request.form['username']
        password = request.form['password']

        # Connessione to database SQLite
        conn = sqlite3.connect('mortenera.sqlite')
        cursor = conn.cursor()

        # build query
        query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
        print(query)
        # execute  query
        cursor.execute(query)
        user = cursor.fetchone()

        # Close connection
        conn.close()

        # Check if user exists
        if user:
            session['username'] = username
            return redirect(url_for('area_riservata', user=username))
        else:
            return 'Credenziali non valide.'
    except Exception as e:
        print(e)
        return 'Errore durante il login.'

@app.route('/area_riservata')
def area_riservata():
    # Ottieni il parametro user dall'URL
    user = session.get('username')
    if user:
        return render_template('area_riservata.html', user=user)
    else:
        return 'Accesso negato.'

if __name__ == '__main__':
    app.run(debug=True)
