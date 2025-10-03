from flask import Flask, render_template, request, redirect, url_for, flash

# Initialisation 
site = Flask(__name__)
site.secret_key = "secret_key_for_flashing"


# Route d'accueil
@site.route("/")
def bonjour():

    # affichage
    return render_template("page_arrive.html")


def add_infos (nom, prenom, nom_utilisateur, mot_passe):

    import sqlite3
    con = sqlite3.connect("info_idividu.db")
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS information (
            nom TEXT,
            prenom TEXT,
            id TEXT,
            mot_passe TEXT,
            nb_personne INTEGER,
            jour TEXT,
            heure TEXT
        )
    """)

    cur.execute("INSERT INTO information (nom, prenom, id, mot_passe) VALUES(?, ?, ?, ?)", (nom, prenom, nom_utilisateur, mot_passe))
    # print(nom, prenom, nom_utilisateur, mot_passe)

    con.commit()
    con.close()


def compar_infos ()


@site.route("/submit", methods=["POST", "GET"])        # page s'inscrire
def submit_and_verify():
    
    prenom = request.form.get("prenom")
    nom = request.form.get("nom")
    nom_utilisateur = request.form.get("nom_utilisateur")
    mot_passe = request.form.get("mot_passe")

    if not all([nom, prenom, nom_utilisateur, mot_passe]):
        flash("Tous les champs doivent être remplis !", "error")
        return redirect(url_for("bonjour"))
    
    add_infos(prenom, nom, nom_utilisateur, mot_passe)
    
    return render_template("connexion.html")

@site.route("/pageprincipale/inscription", methods=["GET"])
def direction_inscription() :
    return render_template("inscription.html")

@site.route("/pageprincipale/connexion", methods=["GET"])
def direction_connexion():
    return render_template("connexion.html")


@site.route("/page_principale", methods=["POST", "GET"])   # page de connection
def direction_page_arrive():

    return render_template("page_principale.html")


# Exécution
if __name__ == '__main__':
    site.run(debug=True)