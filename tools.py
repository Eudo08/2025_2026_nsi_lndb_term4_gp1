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
    
def add_info(colonne, valeur, id_perso):
    sql = f"UPDATE info SET {colonne} = ? WHERE id = ?"
    cur.execute(sql, (valeur, id_perso))
    con.commit()

def get_colonne (colonne):
    sql = f"SELECT {colonne} FROM info"
    cur.execute(sql)
    rows = cur.fetchall()
    return [row[0] for row in rows]

def compar_infos_dej_essaie (valeurs):
    cur.execute ("SELECT id FROM info WHERE nb_personne = ?", (valeurs,))
    ids = [r[0] for r in cur.fetchall()]
    return ids

def compar_infos_dej (colonne, valeurs):
    colonnes_autorisees = {"nb_personne", "jour", "heure"}
    if colonne not in colonnes_autorisees:
        raise ValueError(f"Colonne non autorisée : {colonne}")

    query = f"SELECT id FROM info WHERE {colonne} = ?"
    cur.execute(query, (valeurs,))
    ids = [r[0] for r in cur.fetchall()]
    return ids






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
print (compar_infos_dej ("nb_personne", 4))

