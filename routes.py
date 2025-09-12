from flask import Flask, render_template, request, redirect, url_for, flash


# Initialisation de l'application Flask
site = Flask(__name__)
site.secret_key = "secret_key_for_flashing"





# Route d'accueil
@site.route("/")
def bonjour():

    # Afficher la page d'accueil avec les valeurs par défaut
    return render_template("inscription.html")

@site.route("/submit", methods=["POST", "GET"])
def submit_and_verify():
    prenom = request.form.get("prenom")
    nom = request.form.get("nom")
    nom_utilisateur = request.form.get("nom_utilisateur")
    mot_passe = request.form.get("mot_passe")

    if not all([prenom, nom, nom_utilisateur, mot_passe]):
        flash("Tous les champs doivent être remplis !", "error")
        return redirect(url_for("bonjour"))

# Exécuter l'application Flask
if __name__ == '__main__':
    site.run(debug=True)
