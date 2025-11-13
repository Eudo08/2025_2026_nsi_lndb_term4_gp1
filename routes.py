from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
con = sqlite3.connect("info_idividu.db",check_same_thread=False)
cur = con.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS planning (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        jour TEXT,
        heure TEXT,
        nb_personne INTEGER,
        FOREIGN KEY(user_id) REFERENCES information(id)
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


def creation_pers(nom, prenom, nom_utilisateur, mot_passe):
    cur.execute(
        "INSERT INTO information (nom, prenom, username, mot_de_passe) VALUES(?, ?, ?, ?)",
        (nom, prenom, nom_utilisateur, mot_passe)
    )
    con.commit()
    return cur.lastrowid

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
    
    user_id = creation_pers(nom, prenom, nom_utilisateur, mot_passe)
    session['user_id'] = user_id
    
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
        session['user_id'] = ids_username[0]
        return render_template("page_principale.html") 

    else:
        return redirect("/page_arrive/connexion?error=2")  


    
    # return render_template("connexion.html", error=error)    # c'est quoi ?


 
# @site.route("/page_principale", methods=["POST", "GET"])
# def direction_principale():
#     return render_template("page_principale.html")

def check_personnes_heure_jours(heure_jour, personnes):
    if not heure_jour and personnes:
        return False
    
    if heure_jour and not personnes:
        return False
   
    if not heure_jour and not personnes:
        return None
   
    return True
@site.route("/page_confirmation", methods=["POST", "GET"])
def direction_confirmation():
    id_perso = session.get('user_id')

    if request.method == "POST":
        jours_donnees = {
            "lundi": {
                "heure": request.form.get("lundi_horaires"),
                "nb": request.form.get("lundi_nombre_de_personnes"),
            },
            "mardi": {
                "heure": request.form.get("mardi_horaires"),
                "nb": request.form.get("mardi_nombre_de_personnes"),
            },
            "mercredi": {
                "heure": request.form.get("mercredi_horaires"),
                "nb": request.form.get("mercredi_nombre_de_personnes"),
            },
            "jeudi": {
                "heure": request.form.get("jeudi_horaires"),
                "nb": request.form.get("jeudi_nombre_de_personnes"),
            },
            "vendredi": {
                "heure": request.form.get("vendredi_horaires"),
                "nb": request.form.get("vendredi_nombre_de_personnes"),
            },
        }

        for jour, infos in jours_donnees.items():
            if check_personnes_heure_jours(infos["heure"], infos["nb"]) is False:
                return redirect("/page_principalev2?error=1")

        for jour, infos in jours_donnees.items():
            if infos["heure"] and infos["nb"]:
                add_info("jour", jour, id_perso)
                add_info("nb_personne", infos["nb"], id_perso)
                add_info("heure", infos["heure"], id_perso)

        return render_template(
            "confirmation.html",
            **{f"{jour}_heure": infos["heure"] for jour, infos in jours_donnees.items()},
            **{f"{jour}_nb_personne": infos["nb"] for jour, infos in jours_donnees.items()},
        )
# @site.route("/page_confirmation", methods=["POST", "GET"])
# def direction_confirmation():
#     id_perso = session.get('user_id')
#     if request.method == "POST":

#         lundi_heure = request.form.get("lundi_horaires")
#         mardi_heure = request.form.get("mardi_horaires")
#         mercredi_heure = request.form.get("mercredi_horaires")
#         jeudi_heure = request.form.get("jeudi_horaires")
#         vendredi_heure = request.form.get("vendredi_horaires")

#         lundi_nb_personne = request.form.get("lundi_nombre_de_personnes")
#         mardi_nb_personne = request.form.get("mardi_nombre_de_personnes")
#         mercredi_nb_personne = request.form.get("mercredi_nombre_de_personnes")
#         jeudi_nb_personne = request.form.get("jeudi_nombre_de_personnes")
#         vendredi_nb_personne = request.form.get("vendredi_nombre_de_personnes")

#         if check_personnes_heure_jours(lundi_heure, lundi_nb_personne) == False:
#             return redirect("/page_principalev2?error=1")
#         if check_personnes_heure_jours(mardi_heure, mardi_nb_personne) == False:
#             return redirect("/page_principalev2?error=1")
#         if check_personnes_heure_jours(mercredi_heure, mercredi_nb_personne) == False:
#             return redirect("/page_principalev2?error=1")
#         if check_personnes_heure_jours(jeudi_heure, jeudi_nb_personne) == False:
#             return redirect("/page_principalev2?error=1")
#         if check_personnes_heure_jours(vendredi_heure, vendredi_nb_personne) == False:
#             return redirect("/page_principalev2?error=1")
        
#         jours = [lundi_heure, mardi_heure, mercredi_heure, jeudi_heure, vendredi_heure]
#         nb = [lundi_nb_personne, mardi_nb_personne, mercredi_nb_personne, jeudi_nb_personne, vendredi_nb_personne]
#         for j in jours :

#             if lundi_heure != "" :
#                 add_info ("jour", 'lundi', id_perso)
#                 add_info ("nb_personne", lundi_nb_personne, id_perso)
#                 add_info ("heure", lundi_heure, id_perso)

#             if mardi_heure != "" :
#                 add_info ("jour", 'mardi', id_perso)
#                 add_info ("nb_personne", mardi_nb_personne, id_perso)
#                 add_info ("heure", mardi_heure, id_perso)

#             if mercredi_heure != "" :
#                 add_info ("jour", 'mercredi', id_perso)
#                 add_info ("nb_personne", mercredi_nb_personne, id_perso)
#                 add_info ("heure", mercredi_heure, id_perso)

#             if jeudi_heure != "" :
#                 add_info ("jour", 'jeudi', id_perso)
#                 add_info ("nb_personne", jeudi_nb_personne, id_perso)
#                 add_info ("heure", jeudi_heure, id_perso)

#             if vendredi_heure != "" :
#                 add_info ("jour", 'vendredi', id_perso)
#                 add_info ("nb_personne", vendredi_nb_personne, id_perso)
#                 add_info ("heure", vendredi_heure, id_perso)
            
#         return render_template(
#             "confirmation.html",
#             lundi_heure=lundi_heure,
#             mardi_heure=mardi_heure,
#             mercredi_heure=mercredi_heure,
#             jeudi_heure=jeudi_heure,
#             vendredi_heure=vendredi_heure,
#             lundi_nb_personne=lundi_nb_personne,
#             mardi_nb_personne=mardi_nb_personne,
#             mercredi_nb_personne=mercredi_nb_personne,
#             jeudi_nb_personne=jeudi_nb_personne,
#             vendredi_nb_personne=vendredi_nb_personne
#         )





# Exécution
if __name__ == '__main__':
    site.run(debug=True)