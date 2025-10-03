from flask import Flask, render_template, request, redirect, url_for, flash
# from data import infos_perso
# from tools import add_infos

# Initialisation 
site = Flask(__name__)
site.secret_key = "secret_key_for_flashing"

# Route d'accueil
@site.route("/")
def bonjour():

    # affichage
    return render_template("page_arrive.html")


# def save_info_in_list (liste, prenom, nom, nom_utilisateur, mot_passe):
#     liste = []
#     liste.append([prenom, nom, nom_utilisateur, mot_passe])

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
    print(nom, prenom, nom_utilisateur, mot_passe)

    con.commit()
    con.close()


@site.route("/submit", methods=["POST", "GET"])
def submit_and_verify():
    
    prenom = request.form.get("prenom")
    nom = request.form.get("nom")
    nom_utilisateur = request.form.get("nom_utilisateur")
    mot_passe = request.form.get("mot_passe")

    # infos_perso.append((prenom, nom, nom_utilisateur, mot_passe))
    # print(infos_perso)

    if not all([nom, prenom, nom_utilisateur, mot_passe]):
        flash("Tous les champs doivent être remplis !", "error")
        return redirect(url_for("bonjour"))
    
    # infos_perso.append((prenom, nom, nom_utilisateur, mot_passe))
    add_infos(prenom, nom, nom_utilisateur, mot_passe)
    
    return render_template("connexion.html")

@site.route("/pageprincipale/inscription", methods=["GET"])
def direction_inscription() :
    return render_template("inscription.html")

@site.route("/pageprincipale/connexion", methods=["GET"])
def direction_connexion():
    return render_template("connexion.html")

@site.route("/page_principale", methods=["GET"])
def direction_page_arrive():
    return render_template("page_principale.html")

# Exécution
if __name__ == '__main__':
    site.run(debug=True)