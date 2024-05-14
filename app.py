from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

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
            return render_template('area_riservata.html')
        else:
            return 'Credenziali non valide.'
    except Exception as e:
        print(e)
        return 'Errore durante il login.'



if __name__ == '__main__':
    app.run(debug=True)
