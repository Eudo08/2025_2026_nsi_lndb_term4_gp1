from flask import Flask, render_template, request, redirect, session
import sqlite3
con = sqlite3.connect("info_idividu.db",check_same_thread=False)
cur = con.cursor()

cur.executescript("""
    CREATE TABLE IF NOT EXISTS information (
        id INTEGER PRIMARY KEY,
        nom TEXT,
        prenom TEXT,
        username TEXT UNIQUE,
        mot_de_passe TEXT
    );

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
site.secret_key = "JeanPartickDeLaBruyere"

@site.route("/")       
def home():
    return render_template("page_arrive.html")






# Route d'accueil
@site.route("/page_arrive")      
def bonjour():

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

def add_planning(user_id, jour, heure, nb_personne):
    cur.execute("""
        INSERT INTO planning (user_id, jour, heure, nb_personne)
        VALUES (?, ?, ?, ?)
    """, (user_id, jour, heure, nb_personne))
    con.commit()

def compar_infos_dej (colonne, valeurs):
    colonnes_autorisees = {"nb_personne", "jour", "heure"}
    if colonne not in colonnes_autorisees:
        raise ValueError(f"Colonne non autorisée : {colonne}")

    query = f"SELECT id FROM planning WHERE {colonne} = ?"
    cur.execute(query, (valeurs,))
    ids = [r[0] for r in cur.fetchall()]
    return ids

def select_info_perso (id):
    cur.execute("SELECT prenom, nom FROM information WHERE id = ?", (id,))
    personne = cur.fetchone()
    return personne

def check_personnes_heure_jours(heure_jour, personnes):
    if not heure_jour and personnes:
        return False
    
    if heure_jour and not personnes:
        return False
   
    if not heure_jour and not personnes:
        return None
   
    return True

# Dans votre fichier de gestion de base de données (ex: db_utils.py)

def mark_as_booked(person_id, jour, heure):
    sql = """
    UPDATE planning
    SET is_booked = 1
    WHERE id_perso = ? AND jour = ? AND heure = ?
    """
    cur.execute(sql, (person_id, jour, heure))
    con.commit()
    con.close()
    
    return True



@site.route("/submit", methods=["POST", "GET"])      
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
    if "user_id" in session:
        return render_template("page_principale.html")

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
            valid = check_personnes_heure_jours(infos["heure"], infos["nb"])

            if valid is False:
                return redirect("/page_principalev2?error=1")

            if valid is None:
                infos["nb"] = "aucune sélection"

        # for jour, infos in jours_donnees.items():
        #     if infos["heure"] and infos["nb"]:
        #         add_planning(id_perso, jour, infos["heure"], infos["nb"])
        session['planning_temp'] = jours_donnees

        return render_template(
            "confirmation.html",
            **{f"{jour}_heure": infos["heure"] for jour, infos in jours_donnees.items()},
            **{f"{jour}_nb_personne": infos["nb"] for jour, infos in jours_donnees.items()}, jours=jours_donnees
        )
    error = request.args.get("error")
    return render_template("confirmation.html", erreur=error)


@site.route("/page_finale", methods=["POST", "GET"])
def direction_page_final ():
    id_perso = session.get('user_id')
    can_eat = True
    ids_person = []
    person = []

    jours_donnees = session.get("planning_temp", {})

   # for jour, infos in jours_donnees.items():
   #    if check_personnes_heure_jours(infos["heure"], infos["nb"]) is False:
   #       return redirect("/page_principalev2?error=1")

    for jour, infos in jours_donnees.items():
        
        heure = infos["heure"]
        nb = int(infos["nb"])
        needed = nb - 1

        liste_jours = compar_infos_dej("jour", jour)
        liste_heures = compar_infos_dej("heure", infos["heure"])
        liste_nb = compar_infos_dej("nb_personne", infos["nb"])

        print("DEBUG", jour, liste_jours, liste_heures, liste_nb)

        if not liste_jours or not liste_heures or not liste_nb:
            return redirect("/page_confirmation?error=2")

        if set(liste_jours) == set(liste_heures) == set(liste_nb):
            return redirect("/page_confirmation?error=2")
        
        ids_all_person = liste_jours.copy()
        if id_perso in ids_all_person:
            ids_all_person.remove(id_perso)

        if len(ids_all_person) < needed:
            return redirect("/page_confirmation?error=3")
        ids_person.extend(ids_all_person[:needed])

            # try:

            #     if infos["nb"] == 2 and len(ids_all_person) >= 1:
            #         ids_person.append(ids_all_person.pop())
                
            #     elif infos["nb"] == 4 and len(ids_all_person) >= 3:
            #         ids_person.append(ids_all_person.pop())
            #         ids_person.append(ids_all_person.pop()) 
            #         ids_person.append(ids_all_person.pop())

            #     elif not (infos["nb"] == 2 or infos["nb"] == 4):
            #         pass 
            #     else:
            #         raise IndexError("Pas assez de personnes disponibles")
                

            # except IndexError:
            #     can_eat = False
            #     return redirect("/page_confirmation?error=3")
            
    for jour, infos in jours_donnees.items():
        add_planning(id_perso, jour, infos["heure"], infos["nb"])

    # if not can_eat:
    #     return redirect("/page_confirmation?error=3")
    
    for p in ids_person:
        person.append(select_info_perso(p))
   
    session.pop("planning_temp", None)
    print (person)
    return render_template("page_finale.html", person=person)

@site.route("/retour_page_principale", methods=["POST", "GET"])
def bouton_retour ():
    return render_template ("page_principale.html")

# Exécution
if __name__ == '__main__':
    site.run(debug=True)