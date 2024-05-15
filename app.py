from flask import Flask, render_template, request, redirect, url_for, session
from functools import wraps
from form import LoginForm
import secrets
import sqlite3

# Session key generated randomly
secrets_key = secrets.token_hex(16)
app = Flask(__name__)
app.secret_key = secrets_key

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated_function

#route for page of index
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/public_login', methods=['GET', 'POST'])
def public_login():
    form = LoginForm()
    if form.validate_on_submit():
        pass
    return render_template('public_login.html', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
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
@login_required
def area_riservata():
    # Ottieni il parametro user dall'URL
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
    app.run(debug=True)
