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

@site.route("/")       
def home():
    return render_template("page_arrive.html")

# Route d'accueil
@site.route("/page_arrive")        # page d'accueil
def bonjour():

    # affichage
    return render_template("page_arrive.html")


def creation_pers (nom, prenom, nom_utilisateur, mot_passe):

    cur.execute("INSERT INTO information (nom, prenom, username, mot_de_passe) VALUES(?, ?, ?, ?)", (nom, prenom, nom_utilisateur, mot_passe))
    id = cur.lastrowid
    con.commit()
    return id

def compar_username_motdepasse (colonne, valeurs):
    colonnes_autorisees = {"username", "mot_de_passe"}
    if colonne not in colonnes_autorisees:
        raise ValueError(f"Colonne non autorisée : {colonne}")

    query = f"SELECT id FROM information WHERE {colonne} = ?"
    cur.execute(query, (valeurs,))
    ids = [r[0] for r in cur.fetchall()]
    return ids

def add_info (colonne, valeur, id_perso):
    sql = f"UPDATE information SET {colonne} = ? WHERE id = ?"
    cur.execute(sql, (valeur, id_perso))
    con.commit()

def compar_infos_dej (colonne, valeurs):
    colonnes_autorisees = {"nb_personne", "jour", "heure"}
    if colonne not in colonnes_autorisees:
        raise ValueError(f"Colonne non autorisée : {colonne}")

    query = f"SELECT id FROM information WHERE {colonne} = ?"
    cur.execute(query, (valeurs,))
    ids = [r[0] for r in cur.fetchall()]
    return ids




@site.route("/submit", methods=["POST", "GET"])        # page s'inscrire
def submit_and_verify():
    
    prenom = request.form.get("prenom")
    nom = request.form.get("nom")
    nom_utilisateur = request.form.get("nom_utilisateur")
    mot_passe = request.form.get("mot_passe")

    if not all([nom, prenom, nom_utilisateur, mot_passe]):
        return redirect("/page_arrive/inscription?error=1")
    
    creation_pers(prenom, nom, nom_utilisateur, mot_passe)
    
    return render_template("connexion.html")


@site.route("/page_arrive/inscription", methods=["GET"])
def direction_inscription() :                         
    return render_template("inscription.html")


@site.route("/page_arrive/connexion", methods=["GET"])
def direction_connexion():
    return render_template("connexion.html")

@site.route("/page_principalev2", methods=["POST", "GET"])
def direction_page_arrive():
    
    nom_utilisateur = request.form.get("nom_utilisateur")
    mot_passe = request.form.get("mot_passe")

    if not nom_utilisateur or not mot_passe:
        return redirect("/page_arrive/connexion?error=1")

    ids_username = compar_username_motdepasse("username", nom_utilisateur)
    ids_password = compar_username_motdepasse("mot_de_passe", mot_passe)


    if ids_username and ids_password and ids_username[0] == ids_password[0]:
        return render_template("page_principale.html") 

    else:
        return redirect("/page_arrive/connexion?error=2")  


    
    # return render_template("connexion.html", error=error)    # c'est quoi ?


 
# @site.route("/page_principale", methods=["POST", "GET"])
# def direction_principale():
#     return render_template("page_principale.html")


@site.route("/page_confirmation", methods=["POST", "GET"])
def direction_confirmation():
    if request.method == "POST":
        
        lundi_heure = request.form.get("lundi_horaires")
        mardi_heure = request.form.get("mardi_horaires")
        mercredi_heure = request.form.get("mercredi_horaires")
        jeudi_heure = request.form.get("jeudi_horaires")
        vendredi_heure = request.form.get("vendredi_horaires")
        lundi_nb_personne = request.form.get("lundi_nombre_de_personnes")
        mardi_nb_personne = request.form.get("mardi_nombre_de_personnes")
        mercredi_nb_personne = request.form.get("mercredi_nombre_de_personnes")
        jeudi_nb_personne = request.form.get("jeudi_nombre_de_personnes")
        vendredi_nb_personne = request.form.get("vendredi_nombre_de_personnes")

    return render_template("confirmation.html",  nb_personne=nb_personne, jour=jour, heure=heure)




# Exécution
if __name__ == '__main__':
    site.run(debug=True)