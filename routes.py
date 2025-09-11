from flask import Flask, render_template, request, redirect, url_for, flash
from tools_json import load_data, save_data

# Initialisation de l'application Flask
site = Flask(__name__)
site.secret_key = "secret_key_for_flashing"


FILE_PATH = 'data.json'  # Chemin du fichier de données


# Route d'accueil
@site.route("/")
def bonjour():

    # Afficher la page d'accueil avec les valeurs par défaut
    return render_template("page_arrive.html")




# Exécuter l'application Flask
if __name__ == '__main__':
    site.run(debug=True)
