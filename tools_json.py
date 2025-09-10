import json

# Chemin du fichier de données JSON
FILE_PATH = 'data.json'

# Fonction pour charger les données depuis le fichier JSON
def load_data():
    try:
        with open(FILE_PATH, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


# Fonction pour sauvegarder les données dans le fichier JSON
def save_data(data):
    with open(FILE_PATH, 'w') as file:
        json.dump(data, file, indent=4)
