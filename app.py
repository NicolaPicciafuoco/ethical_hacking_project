from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    try:
        # Ricevi i dati dalla richiesta POST
        username = request.form['username']
        password = request.form['password']

        # Connessione al database SQLite
        conn = sqlite3.connect('mortenera.sqlite')
        cursor = conn.cursor()

        # Costruisci la query con la concatenazione diretta dei valori dell'utente
        query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
        print(query)
        # Esegui la query
        cursor.execute(query)
        user = cursor.fetchone()

        # Chiudi la connessione al database
        conn.close()

        # Se l'autenticazione ha successo, restituisci il messaggio di login riuscito
        if user:
            return render_template('index.html')
        else:
            return 'Credenziali non valide.'
    except Exception as e:
        print(e)
        return 'Errore durante il login.'


if __name__ == '__main__':
    app.run(debug=True)
