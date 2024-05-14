import sqlite3

# Connessione al database
conn = sqlite3.connect('mortenera.sqlite')
cursor = conn.cursor()

# Esempio di query per ottenere le credenziali utente
username = input("Inserisci il nome utente: ")
password = input("Inserisci la password: ")

# Esempio di query per ottenere le credenziali utente
query = "SELECT * FROM users WHERE username = ? AND password = ?"
cursor.execute(query, (username, password))
user = cursor.fetchone()

if user:
    print("Accesso riuscito!")
    # Qui puoi eseguire le azioni che desideri dopo il login
else:
    print("Credenziali non valide.")

# Chiusura della connessione
conn.close()
