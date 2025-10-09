from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
con = sqlite3.connect("info_idividu.db",check_same_thread=False)
cur = con.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS information (
        id INTEGER PRIMARY KEY,
        nom TEXT,
        prenom TEXT,
        username TEXT UNIQUE,
        mot_de_passe TEXT,
        nb_personne INTEGER,
        jour TEXT,
        heure TEXT
    )
""")

# Initialisation 
site = Flask(__name__)
site.secret_key = "secret_key_for_flashing"


# Route d'accueil
@site.route("/")        # page d'accueil
def bonjour():

    # affichage
    return render_template("page_arrive.html")


def creation_pers (nom, prenom, nom_utilisateur, mot_passe):

    cur.execute("INSERT INTO information (nom, prenom, username, mot_de_passe) VALUES(?, ?, ?, ?)", (nom, prenom, nom_utilisateur, mot_passe))
    # print(nom, prenom, nom_utilisateur, mot_passe)

    con.commit()
    con.close()



def add_info (collonne, ligne, info):      # Pour ajouter le jour, l'heure et le nombre de personne
    cur.execute("INSERT INTO information (?) VALUES(?) WHERE id = ?", (collonne, info, ligne))

def compar_infos_dej (nb_personne, jour, heure):
    pass
    

@site.route("/submit", methods=["POST", "GET"])        # page s'inscrire
def submit_and_verify():
    
    prenom = request.form.get("prenom")
    nom = request.form.get("nom")
    nom_utilisateur = request.form.get("nom_utilisateur")
    mot_passe = request.form.get("mot_passe")

    if not all([nom, prenom, nom_utilisateur, mot_passe]):
        flash("Tous les champs doivent être remplis !", "error")
        return redirect("/page_arrive/inscription?error=1")
    
    creation_pers(prenom, nom, nom_utilisateur, mot_passe)
    
    return render_template("connexion.html")

@site.route("/page_arrive/inscription", methods=["GET"])
def direction_inscription() :
    return render_template("inscription.html")

@site.route("/page_arrive/connexion", methods=["GET"])
def direction_connexion():
    return render_template("connexion.html")

@site.route("/page_principalev2", methods=["POST", "GET"])   # page de connection
def direction_page_arrive():
    if request.method == "POST":
        nom_utilisateur = request.form.get("nom_utilisateur")
        mot_passe = request.form.get("mot_passe")

        if not nom_utilisateur or not mot_passe:
            return redirect("/page_arrive/connexion?error=1")

        redirection = compar_infos_connection(nom_utilisateur, mot_passe)
        if redirection:
            return redirection
        else:
            return redirect("/page_arrive/connexion?error=2")

    error = request.args.get("error")
    return render_template("connexion.html", error=error)


def compar_infos_connection (nom_utilisateur, mot_passe):
    page = redirect("page_arrive.html")
    cur.execute("SELECT username, mot_de_passe FROM information")
    if nom_utilisateur == "username" and mot_passe == "mot_de_passe" :
        return page
    


 
@site.route("/page_principale", methods=["POST", "GET"])
def direction_principale():
    return render_template("page_principale.html")

# Exécution
if __name__ == '__main__':
    site.run(debug=True)