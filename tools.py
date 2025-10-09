import sqlite3
con = sqlite3.connect("info_idividu.db",check_same_thread=False)
cur = con.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS info (
        nom TEXT,
        prenom TEXT,
        nb_personne INTEGER,
        jour TEXT,
        heure TEXT
    )
""")

def creation_pers (nom, prenom):

    cur.execute("INSERT INTO info (nom, prenom) VALUES(?, ?)", (nom, prenom))
    # print(nom, prenom, nom_utilisateur, mot_passe)

    con.commit()
    con.close()

def add_info (collonne, ligne, info):      # Pour ajouter le jour, l'heure et le nombre de personne
    cur.execute("INSERT INTO info (?) VALUES(?) WHERE id = ?", (collonne, info, ligne))

def compar_infos_dej (nb_pers_voulu):
    cur.execute("SELECT nb_personne FROM info")
    if nb_pers_voulu == "nb_personne":
        return True
    else : 
        return False
    



creation_pers("abc", "adren")
add_info("nb_personne", "adrien", 4)
creation_pers("aze", "Gabriel")
add_info("nb_personne", "Gabriel", 2)
print (compar_infos_dej (4))

