import sqlite3
con = sqlite3.connect("essaie.db",check_same_thread=False)
cur = con.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS info (
        id INTEGER PRIMARY KEY,
        nom TEXT,
        prenom TEXT,
        nb_personne INTEGER,
        jour TEXT,
        heure TEXT
    )
""")

def creation_pers (nom, prenom):

    cur.execute("INSERT INTO info (nom, prenom) VALUES(?, ?)", (nom, prenom))
    id = cur.lastrowid
    con.commit()
    return id
    
def add_info (colonne, valeur, id_perso):
    sql = f"UPDATE info SET {colonne} = ? WHERE id = ?"
    cur.execute(sql, (valeur, id_perso))
    con.commit()

def get_colonne (colonne):             # Pas copier
    sql = f"SELECT {colonne} FROM info"
    cur.execute(sql)
    rows = cur.fetchall()
    return [row[0] for row in rows]

def compar_username_motdepasse (colonne, valeurs):
    colonnes_autorisees = {"username", "mot_de_passe"}
    if colonne not in colonnes_autorisees:
        raise ValueError(f"Colonne non autorisée : {colonne}")

    query = f"SELECT id FROM info WHERE {colonne} = ?"
    cur.execute(query, (valeurs,))
    ids = [r[0] for r in cur.fetchall()]
    return ids

# def compar_infos_dej_essaie (valeurs):
#     cur.execute ("SELECT id FROM info WHERE nb_personne = ?", (valeurs,))
#     ids = [r[0] for r in cur.fetchall()]
#     return ids

def compar_infos_dej (colonne, valeurs):
    colonnes_autorisees = {"nb_personne", "jour", "heure"}
    if colonne not in colonnes_autorisees:
        raise ValueError(f"Colonne non autorisée : {colonne}")

    query = f"SELECT id FROM info WHERE {colonne} = ?"
    cur.execute(query, (valeurs,))
    ids = [r[0] for r in cur.fetchall()]
    return ids

def transforme_id_in_name (ids):         # Pas copier
    names = []
    for i in ids :
        query = f"SELECT prenom FROM info WHERE id == {i}"
        cur.execute(query)
        names = names + [r[0] for r in cur.fetchall()]
    return names




# # sql = f"SELECT {colonne} FROM info WHERE nb_personne = ?"
# # cur.execute(sql, (nb_pers_voulu))
# resultats = cur.fetchall()
# for resultat in resultats:
#     print(resultat)
# # if nb_pers_voulu == sql:
# #     return True
# # else : 
# #     return False
    


# id = creation_pers("vfr", "bgt")
# add_info("nb_personne", 4, id)
# id = creation_pers("edodo", "eudo")
# add_info("nb_personne", 3, id)

# print (get_colonne ("prenom"))
print (transforme_id_in_name(compar_infos_dej ("nb_personne", 5)))





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


    # lundi_heure = request.form.get("lundi_horaires")
    # mardi_heure = request.form.get("mardi_horaires")
    # mercredi_heure = request.form.get("mercredi_horaires")
    # jeudi_heure = request.form.get("jeudi_horaires")
    # vendredi_heure = request.form.get("vendredi_horaires")

    # lundi_nb_personne = request.form.get("lundi_nombre_de_personnes")
    # mardi_nb_personne = request.form.get("mardi_nombre_de_personnes")
    # mercredi_nb_personne = request.form.get("mercredi_nombre_de_personnes")
    # jeudi_nb_personne = request.form.get("jeudi_nombre_de_personnes")
    # vendredi_nb_personne = request.form.get("vendredi_nombre_de_personnes")

# jours = [lundi_heure, mardi_heure, mercredi_heure, jeudi_heure, vendredi_heure]

# for j in jours :
# if lundi_heure != "" :
# add_info (jour, lundi, id_perso)
# add_info (nb_personne, lundi_nb_personne, id_perso)
# add_info (heure, lundi_heure, id_perso)

# if mardi_heure != "" :
# add_info (jour, mardi, id_perso)
# add_info (nb_personne, mardi_nb_personne, id_perso)
# add_info (heure, mardi_heure, id_perso)

# if mercredi_heure != "" :
# add_info (jour, mercredi, id_perso)
# add_info (nb_personne, mercredi_nb_personne, id_perso)
# add_info (heure, mercredi_heure, id_perso)

# if jeudi_heure != "" :
# add_info (jour, jeudi, id_perso)
# add_info (nb_personne, jeudi_nb_personne, id_perso)
# add_info (heure, jeudi_heure, id_perso)

# if vendredi_heure != "" :
# add_info (jour, vendredi, id_perso)
# add_info (nb_personne, vendredi_nb_personne, id_perso)
# add_info (heure, vendredi_heure, id_perso)

# else :
#    

# add_info ("jour", jour, id_perso)
# add_info ("nb_personne", jour_nb_personne, id_perso)
# add_info ("heure", heure, id_perso)


    #     if liste_jours == [] or liste_heures == [] or liste_nb == []:
    #         can_eat = False
    #         break

    #     if liste_jours == liste_heures and liste_heures == liste_nb:
    #         ids_all_person = liste_jours

    #         try:

    #             if infos["nb"] == 2 and len(ids_all_person) >= 1:
    #                 ids_person.append(ids_all_person.pop())
                    
    #             elif infos["nb"] == 4 and len(ids_all_person) >= 3:
    #                 ids_person.append(ids_all_person.pop())
    #                 ids_person.append(ids_all_person.pop()) 
    #                 ids_person.append(ids_all_person.pop())

    #             elif not (infos["nb"] == 2 or infos["nb"] == 4):
    #                 pass 
    #             else:
    #                 raise IndexError("Pas assez de personnes disponibles")
                    

    #         except IndexError:
    #             can_eat = False
    #             return redirect("/page_confirmation?error=3")

    # if not can_eat:
    #     return redirect("/page_confirmation?error=3")
    
    # for p in ids_person:
    #     person.append(select_info_perso(p))
    