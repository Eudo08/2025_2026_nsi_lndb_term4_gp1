from flask import Flask, render_template, request, redirect, url_for, flash
from tools_json import load_data, save_data

# Initialisation de l'application Flask
site = Flask(__name__)
site.secret_key = "secret_key_for_flashing"


FILE_PATH = 'data.json'  # Chemin du fichier de données


# Route d'accueil
@site.route("/")
def bonjour():
    # Valeurs par défaut pour les sliders
    plat = 5
    # Afficher la page d'accueil avec les valeurs par défaut
    return render_template("index.html")




# Exécuter l'application Flask
if __name__ == '__main__':
    site.run(debug=True)
