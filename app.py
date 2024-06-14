from flask import Flask, render_template, request, redirect, url_for, session
from datetime import timedelta
from form import LoginForm
import secrets
import sqlite3
import os
import uuid

# Session key generated randomly
secrets_key = str(uuid.uuid4())
app = Flask(__name__)
app.secret_key = secrets_key
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)



# def login_required(f):
#     """
#     Decorator function to require login for accessing a route.

# This function checks if the 'username' key is present in the session. If not, it redirects the user to the login
# page. If the 'username' key is present, it calls the decorated function.

#     Args:
#         f: The function to be decorated.

#     Returns:
#         The decorated function.

#     """
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if 'username' not in session:
#             return redirect(url_for('login_page'))
#         return f(*args, **kwargs)
#     return decorated_function

#route for page of index
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/public_login', methods=['GET', 'POST'])
def public_login():
    form = LoginForm(request.form)
    if request.method == 'GET':
        return render_template('public_login.html', form=form)
    elif request.method == 'POST' and form.validate():
        try:
            username = form.username.data
            password = form.password.data

            # Connessione al database SQLite
            conn = sqlite3.connect('/home/vagrant/ethical_hacking_project/mortenera.sqlite')
            cursor = conn.cursor()

            # Costruisci la query
            query = "SELECT * FROM users WHERE username = ? AND password = ?"
            # Execute query
            cursor.execute(query, (username, password))
            user = cursor.fetchall()

            # Chiudi la connessione
            conn.close()

            # Controlla se l'utente esiste
            if user:
                session['username'] = username
                session.permanent = True
                return redirect(url_for('area_riservata', user=username))
            else:
                error = 'Credenziali non valide.'
                return render_template('public_login.html', form=form, error=error)
        except Exception as e:
            print(e)
            return 'Errore durante il login.'
    else:
        return render_template('public_login.html', form=form)


@app.route('/keygen', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('staff.html')
    elif request.method == 'POST':
        try:
            #
            username = request.form['username']
            password = request.form['password']

            # Connessione to database SQLite
            conn = sqlite3.connect('/home/vagrant/ethical_hacking_project/mortenera.sqlite')
            cursor = conn.cursor()

            # build query
            query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
            # execute  query
            cursor.execute(query)
            user = cursor.fetchone()

            # Close connection
            conn.close()

            # Check if user exists
            if user:
                session['username'] = username
                session.permanent = True
                return redirect(url_for('area_riservata', user=username))
            else:
                error = 'Credenziali non valide.'
                return render_template('staff.html', error=error)
        except Exception as e:
            print(e)
            return 'Errore durante il login.'


@app.route('/area_riservata')
def area_riservata():
    if 'username' not in session:
        return redirect(url_for('index'))
    user = session.get('username')
    if user:
        return render_template('area_riservata.html', user=user)
    else:
        return 'Accesso negato.'


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
