import itertools
# Function to generate possible passwords
def generate_passwords(nome, cognome, data_di_nascita, luogo_di_nascita=""):
    possible_passwords = []

    # add name and surname
    possible_passwords.extend([nome.lower(), cognome.lower()])
    possible_passwords.extend([nome.lower() + cognome.lower(), cognome.lower() + nome.lower()])

    # Add combinations of name and surname with date of birth
    possible_passwords.extend([nome.lower() + data_di_nascita, cognome.lower() + data_di_nascita])
    possible_passwords.extend([nome.lower() + cognome.lower() + data_di_nascita, cognome.lower() + nome.lower() + data_di_nascita])

    # add combinations of name, surname and place of birth
    if luogo_di_nascita:
        possible_passwords.extend([nome.lower() + cognome.lower() + luogo_di_nascita, cognome.lower() + nome.lower() + luogo_di_nascita])

    # add numbers and symbols
    variants = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '!', '@', '#', '$', '%']
    possible_passwords.extend([password + variant for password, variant in itertools.product(possible_passwords, variants)])

    return possible_passwords

# Info on the user
nome = "Alice"
cognome = "Leovince"
data_di_nascita = "01122000"
luogo_di_nascita = ""

# generation of possible passwords
possibili_passwords = generate_passwords(nome, cognome, data_di_nascita, luogo_di_nascita)

# to do impelment save in file
print("Possibili password:")
for password in possibili_passwords:
    print(password)
