from flask import Flask, render_template, request, redirect, url_for, flash
from data import infos_perso

# Initialisation 
site = Flask(__name__)
site.secret_key = "secret_key_for_flashing"



# Route d'accueil
@site.route("/")
def bonjour():

    # affichage
    return render_template("page_arrive.html")


def save_info_in_list (liste, prenom, nom, nom_utilisateur, mot_passe):
    liste.append([prenom, nom, nom_utilisateur, mot_passe])


@site.route("/submit", methods=["POST", "GET"])
def submit_and_verify():
    
    prenom = request.form.get("prenom")
    nom = request.form.get("nom")
    nom_utilisateur = request.form.get("nom_utilisateur")
    mot_passe = request.form.get("mot_passe")
    
    if not all([prenom, nom, nom_utilisateur, mot_passe]):
        flash("Tous les champs doivent être remplis !", "error")
        return redirect(url_for("bonjour"))
    
    save_info_in_list (infos_perso, prenom, nom, nom_utilisateur, mot_passe)
    
    return render_template("connexion.html")



@site.route("/pageprincipale/inscription", methods=["GET"])
def direction_inscription() :
    return render_template("inscription.html")

@site.route("/pageprincipale/connexion", methods=["GET"])
def direction_connexion():
    return render_template("connexion.html")

# Exécution
if __name__ == '__main__':
    site.run(debug=True)


