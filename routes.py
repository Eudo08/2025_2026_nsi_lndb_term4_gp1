from flask import Flask, render_template, request, redirect, session
import sqlite3
# con = sqlite3.connect("info_idividu.db",check_same_thread=False)
# cur = con.cursor()
import sqlite3

DB_PATH = "info_idividu.db"

def init_db():
    con = sqlite3.connect(DB_PATH)
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
        );

        CREATE TABLE IF NOT EXISTS association (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            jour TEXT,
            autre_id INTEGER,
            FOREIGN KEY(user_id) REFERENCES information(id),
            FOREIGN KEY(autre_id) REFERENCES information(id)
        );
    """)
    con.commit()
    con.close()


# cur.executescript("""
#     CREATE TABLE IF NOT EXISTS information (
#         id INTEGER PRIMARY KEY,
#         nom TEXT,
#         prenom TEXT,
#         username TEXT UNIQUE,
#         mot_de_passe TEXT
#     );

#     CREATE TABLE IF NOT EXISTS planning (
#         id INTEGER PRIMARY KEY,
#         user_id INTEGER,
#         jour TEXT,
#         heure TEXT,
#         nb_personne INTEGER,
#         FOREIGN KEY(user_id) REFERENCES information(id)
#     );

#     CREATE TABLE IF NOT EXISTS association (
#         id INTEGER PRIMARY KEY,
#         user_id INTEGER,
#         jour TEXT,
#         autre_id INTEGER,
#         FOREIGN KEY(user_id) REFERENCES information(id),
#         FOREIGN KEY(autre_id) REFERENCES information(id)
#     );
# """)

def save_association(user_id, jour, autre_id):
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("""
        INSERT INTO association (user_id, jour, autre_id)
        VALUES (?, ?, ?)
    """, (user_id, jour, autre_id))
    con.commit()
    con.close()


# Initialisation 
site = Flask(__name__)
site.secret_key = "JeanPartickDeLaBruyere"
init_db()

@site.route("/")       
def home():
    return render_template("page_arrive.html")

@site.route("/arrive")       
def acceuil():
    return render_template("page_arrive.html")


# Route d'accueil
@site.route("/page_arrive")      
def bonjour():

    return render_template("page_arrive.html")


def creation_pers(nom, prenom, nom_utilisateur, mot_passe):
    con = get_db_connection()
    cur = con.cursor()
    try:
        cur.execute(
            "INSERT INTO information (nom, prenom, username, mot_de_passe) VALUES(?, ?, ?, ?)",
            (nom, prenom, nom_utilisateur, mot_passe)
        )
        con.commit()
        return cur.lastrowid
    except sqlite3.IntegrityError as e:
        if "UNIQUE constraint failed: information.username" in str(e):
            return None
        raise
    finally:
        con.close()

def compar_username_motdepasse(colonne, valeurs):
    colonnes_autorisees = {"username", "mot_de_passe"}
    if colonne not in colonnes_autorisees:
        raise ValueError(f"Colonne non autorisée : {colonne}")
    con = get_db_connection()
    cur = con.cursor()
    query = f"SELECT id FROM information WHERE {colonne} = ?"
    cur.execute(query, (valeurs,))
    ids = [r[0] for r in cur.fetchall()]
    con.close()
    return ids


def add_planning(user_id, jour, heure, nb_personne):
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("""
        INSERT INTO planning (user_id, jour, heure, nb_personne)
        VALUES (?, ?, ?, ?)
    """, (user_id, jour, heure, nb_personne))
    con.commit()
    con.close()


def compar_infos_dej(colonne, valeurs):
    colonnes_autorisees = {"nb_personne", "jour", "heure"}
    if colonne not in colonnes_autorisees:
        raise ValueError(f"Colonne non autorisée : {colonne}")
    con = get_db_connection()
    cur = con.cursor()
    query = f"SELECT id FROM planning WHERE {colonne} = ?"
    cur.execute(query, (valeurs,))
    ids = [r[0] for r in cur.fetchall()]
    con.close()
    return ids


def select_info_perso(id):
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("SELECT prenom, nom FROM information WHERE id = ?", (id,))
    personne = cur.fetchone()
    con.close()
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

# Si tu ajoutes une colonne:
# ALTER TABLE planning ADD COLUMN is_booked INTEGER DEFAULT 0;

def mark_as_booked(user_id, jour, heure):
    con = get_db_connection()
    cur = con.cursor()
    sql = """
    UPDATE planning
    SET is_booked = 1
    WHERE user_id = ? AND jour = ? AND heure = ?
    """
    cur.execute(sql, (user_id, jour, heure))
    con.commit()
    con.close()
    return True


def get_db_connection():
    # Remplacez ceci par votre propre logique de connexion
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con

def trouver_personnes_correspondantes(jour, heure, nb):
    con = get_db_connection()
    cur = con.cursor()
    query = """
        SELECT user_id 
        FROM planning 
        WHERE jour = ? 
          AND heure = ? 
          AND nb_personne = ?
    """
    cur.execute(query, (jour, heure, nb))
    resultats = cur.fetchall()
    ids_trouves = [row[0] for row in resultats]
    con.close()
    return ids_trouves



@site.route("/submit", methods=["POST", "GET"])      
def submit_and_verify():
    
    prenom = request.form.get("prenom")
    nom = request.form.get("nom")
    nom_utilisateur = request.form.get("nom_utilisateur")
    mot_passe = request.form.get("mot_passe")

    if not all([nom, prenom, nom_utilisateur, mot_passe]):
        return redirect("/page_arrive/inscription?error=1")
    
    user_id = creation_pers(nom, prenom, nom_utilisateur, mot_passe)
    
    if user_id is None:
        return redirect("/page_arrive/inscription?error=3")
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

    print("===== DEBUG CONNEXION =====")
    print("Username saisi:", nom_utilisateur)
    print("Mot de passe saisi:", mot_passe)

    if not nom_utilisateur or not mot_passe:
        return redirect("/page_arrive/connexion?error=1")

    ids_username = compar_username_motdepasse("username", nom_utilisateur)
    ids_password = compar_username_motdepasse("mot_de_passe", mot_passe)

    print("IDs trouvés pour username:", ids_username)
    print("IDs trouvés pour mot de passe:", ids_password)
    print("===========================")

    if ids_username and ids_password and ids_username[0] in ids_password:
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


        session['planning_temp'] = jours_donnees

        return render_template(
            "confirmation.html",
            **{f"{jour}_heure": infos["heure"] for jour, infos in jours_donnees.items()},
            **{f"{jour}_nb_personne": infos["nb"] for jour, infos in jours_donnees.items()}, jours=jours_donnees
        )
    error = request.args.get("error")
    return render_template("confirmation.html", erreur=error)

@site.route("/page_finale", methods=["POST", "GET"])
def direction_page_final():
    id_perso = session.get('user_id')
    if not id_perso:
        return redirect("/page_arrive/connexion")

    jours_donnees = session.get("planning_temp", {})

    personnes_par_jour = {"lundi": [], "mardi": [], "mercredi": [], "jeudi": [], "vendredi": []}

    # Effacer anciennes associations de cet utilisateur
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("DELETE FROM association WHERE user_id = ?", (id_perso,))
    con.commit()
    con.close()

    for jour, infos in jours_donnees.items():
        heure = infos.get("heure")
        nb = infos.get("nb")

        if nb == "aucune sélection" or not heure:
            continue

        try:
            nb = int(nb)
        except ValueError:
            return redirect("/page_confirmation?error=2")

        needed = nb - 1
        ids_all_person = trouver_personnes_correspondantes(jour, heure, nb)

        if id_perso in ids_all_person:
            ids_all_person.remove(id_perso)

        if len(ids_all_person) < needed:
            return redirect("/page_confirmation?error=3")

        ids_choisis = ids_all_person[:needed]

        for pid in ids_choisis:
            info_personne = select_info_perso(pid)
            if info_personne:
                personnes_par_jour[jour].append(info_personne)
                save_association(id_perso, jour, pid)

    # Remplacer le planning de l'utilisateur par le nouveau
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("DELETE FROM planning WHERE user_id = ?", (id_perso,))
    con.commit()
    con.close()

    for jour, infos in jours_donnees.items():
        if infos["nb"] != "aucune sélection":
            add_planning(id_perso, jour, infos["heure"], infos["nb"])

    session.pop("planning_temp", None)

    return render_template("page_finale.html", personnes_par_jour=personnes_par_jour)

# @site.route("/page_finale", methods=["POST", "GET"])
# def direction_page_final():
#     id_perso = session.get('user_id')

#     jours_donnees = session.get("planning_temp", {})

#     # Dictionnaire final : liste des personnes par jour
#     personnes_par_jour = {
#         "lundi": [],
#         "mardi": [],
#         "mercredi": [],
#         "jeudi": [],
#         "vendredi": [],
#     }
#     cur.execute("DELETE FROM association WHERE user_id = ?", (id_perso,))
#     con.commit()
#     # -------------------------------------------------------
#     # 1) TRAITEMENT POUR CHAQUE JOUR
#     # -------------------------------------------------------
#     for jour, infos in jours_donnees.items():
        
#         heure = infos["heure"]
#         nb = infos["nb"]

#         # Aucun choix → on saute ce jour
#         if nb == "aucune sélection" or heure is None or heure == "":
#             continue  

#         # Convertir en int en toute sécurité
#         try:
#             nb = int(nb)
#         except ValueError:
#             return redirect("/page_confirmation?error=2")

#         needed = nb - 1   # ex : 4 → 3 personnes

#         # Recherche des autres personnes
#         # liste_jours = compar_infos_dej("jour", jour)
#         # liste_heures = compar_infos_dej("heure", heure)
#         # liste_nb = compar_infos_dej("nb_personne", nb)

#         ids_all_person = trouver_personnes_correspondantes(jour, heure, nb)

#         print("--------- DEBUG ---------")
#         print("Jour :", jour)
#         print("Critères :", heure, "pour", nb, "personnes")
#         print("IDs trouvés (brut) :", ids_all_person)
#         # print("Nombre :", nb)
#         # print("Liste jours :", liste_jours)
#         # print("Liste heures :", liste_heures)
#         # print("Liste nb :", liste_nb)

#         # # Si une liste est vide → incohérence
#         # if not liste_jours or not liste_heures or not liste_nb:
#         #     return redirect("/page_confirmation?error=2")

#         # # Vérifier que ce sont bien les mêmes personnes
#         # if not (set(liste_jours) == set(liste_heures) == set(liste_nb)):
#         #     return redirect("/page_confirmation?error=2")

#         # # Copie propre
#         # ids_all_person = liste_jours.copy()

#         # Enlever moi-même
#         if id_perso in ids_all_person:
#             ids_all_person.remove(id_perso)

#         # Assez de personnes ?
#         if len(ids_all_person) < needed:
#             return redirect("/page_confirmation?error=3")

#         # On prend les personnes nécessaires
#         ids_choisis = ids_all_person[:needed]

#         print("IDs finallement choisis (après slice) :", ids_choisis)

#         # Récupérer les noms/prénoms
#         for pid in ids_choisis:
#             info_personne = select_info_perso(pid) # ex: {"nom": "Dupont", "prenom": "Jean"}
#             if info_personne: # S'assurer que la personne existe
#                 personnes_par_jour[jour].append(info_personne)
#             save_association(id_perso, jour, pid)
#     # -------------------------------------------------------
#     # 2) Ajout en base APRÈS vérification
#     # -------------------------------------------------------
    
#     # Effacer ancien planning
#     cur.execute("DELETE FROM planning WHERE user_id = ?", (id_perso,))
#     con.commit()

#     for jour, infos in jours_donnees.items():
#         if infos["nb"] != "aucune sélection":
#             add_planning(id_perso, jour, infos["heure"], infos["nb"])

#     # -------------------------------------------------------
#     # 3) Envoie au HTML
#     # -------------------------------------------------------
#     session.pop("planning_temp", None)

#     return render_template("page_finale.html", personnes_par_jour=personnes_par_jour)

# @site.route("/page_finale", methods=["POST", "GET"])
# def direction_page_final ():
#     id_perso = session.get('user_id')
#     can_eat = True
#     ids_person = []
#     person = []

#     jours_donnees = session.get("planning_temp", {})



#     for jour, infos in jours_donnees.items():
        
#         heure = infos["heure"]
#         nb = int(infos["nb"])
#         needed = nb - 1

#         liste_jours = compar_infos_dej("jour", jour)
#         liste_heures = compar_infos_dej("heure", infos["heure"])
#         liste_nb = compar_infos_dej("nb_personne", infos["nb"])

#         print("DEBUG", jour, liste_jours, liste_heures, liste_nb)

#         if not liste_jours or not liste_heures or not liste_nb:
#             return redirect("/page_confirmation?error=2")

#         if set(liste_jours) == set(liste_heures) == set(liste_nb):
#             return redirect("/page_confirmation?error=2")
        
#         ids_all_person = liste_jours.copy()
#         if id_perso in ids_all_person:
#             ids_all_person.remove(id_perso)

#         if len(ids_all_person) < needed:
#             return redirect("/page_confirmation?error=3")
#         ids_person.extend(ids_all_person[:needed])

#     for jour, infos in jours_donnees.items():
#         add_planning(id_perso, jour, infos["heure"], infos["nb"])


    
#     for p in ids_person:
#         person.append(select_info_perso(p))
   
#     session.pop("planning_temp", None)
#     print (person)
#     return render_template("page_finale.html", person=person)

@site.route("/retour_page_principale", methods=["POST", "GET"])
def bouton_retour ():
    return render_template ("page_principale.html")


def get_associations(user_id):
    con = get_db_connection()
    cur = con.cursor()
    query = """
        SELECT jour, autre_id
        FROM association
        WHERE user_id = ?
    """
    cur.execute(query, (user_id,))
    result = cur.fetchall()
    con.close()
    personnes_par_jour = {
        "lundi": [],
        "mardi": [],
        "mercredi": [],
        "jeudi": [],
        "vendredi": []
    }

    for jour, pid in result:
        personne = select_info_perso(pid)
        if personne:
            personnes_par_jour[jour].append(personne)

    return personnes_par_jour

@site.route("/page_groupes", methods=["GET"])
def direction_page_groupes ():
    user_id = session.get("user_id")

    if not user_id:
        return redirect("/page_arrive/connexion")
    association = get_associations(user_id)

    return render_template("groupes.html", associations=association)


@site.route("/deconnexion", methods=["GET"])
def deconnexion():
    session.clear()  # Vide toute la session
    return redirect("/page_arrive")

# Exécution
if __name__ == '__main__':
    site.run(debug=True)