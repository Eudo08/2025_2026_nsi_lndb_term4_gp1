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
    
def add_info (ligne, info, id_perso):      # Pour ajouter le jour, l'heure et le nombre de personne
    cur.execute("INSERT INTO info (?) VALUES(?) WHERE id = ?", (ligne, info, id_perso ))
    con.commit()

def compar_infos_dej (nb_pers_voulu):
    cur.execute("SELECT nb_personne FROM info")
    if nb_pers_voulu == "nb_personne":
        return True
    else : 
        return False
    


id = creation_pers("abc", "adren")
# add_info("nb_personne", 4, id)
creation_pers("aze", "Gabriel")
# add_info("nb_personne", "Gabriel", 2)
# print (compar_infos_dej (4))







# But de la fonction
# Mettre à jour une seule colonne (jour, heure ou nb_personne) d’une ligne existante identifiée par son id dans la table info.

# Signature et paramètres
# def add_info(ligne, info, id_perso):

# ligne : nom de la colonne à mettre à jour; doit appartenir à la liste blanche ALLOWED_COLUMNS.

# info : nouvelle valeur à écrire dans la colonne.

# id_perso : identifiant (id) de la ligne à modifier.

# Liste blanche des colonnes
# ALLOWED_COLUMNS = {"nb_personne", "jour", "heure"}

# Permet d’empêcher l’injection SQL en s’assurant que seules des colonnes connues et autorisées peuvent être modifiées.

# Si ligne n’appartient pas à cette liste, la fonction lève une ValueError et n’exécute pas de requête SQL.

# Construction de la requête

# La requête est construite en concaténant le nom de colonne validé dans le SQL :

# sql = f"UPDATE info SET {ligne} = ? WHERE id = ?"

# Les valeurs sont fournies via paramètres SQL sécurisés (placeholders) : (info, id_perso).

# Raison : les placeholders ne peuvent remplacer que des valeurs, pas des identifiants (nom de colonne), d’où la nécessité de valider la colonne puis de l’insérer directement dans la chaîne SQL.

# Exécution et engagement
# cur.execute(sql, (info, id_perso)) exécute la mise à jour.

# con.commit() applique la modification sur la base de données.

# La fonction retourne cur.rowcount (nombre de lignes affectées) pour indiquer si la mise à jour a réussi (généralement 1) ou si aucune ligne n’a été trouvée (0).

# Sécurité et raisons des choix
# Ne pas permettre que ligne vienne directement de l’utilisateur sans validation : sinon risque d’injection SQL via le nom de colonne.

# Utiliser des placeholders pour les valeurs empêche l’injection SQL au niveau des données.

# Préférer UPDATE plutôt que INSERT quand on veut modifier une ligne existante ; INSERT ajoute une nouvelle ligne et ne prend pas de WHERE.

# Exemples d’utilisation
# Mettre à jour le nombre de personnes pour l’id 1 :

# ALLOWED_COLUMNS = {"nb_personne", "jour", "heure"}

# def add_info(ligne, info, id_perso):
#     if ligne not in ALLOWED_COLUMNS:
#         raise ValueError(f"Nom de colonne invalide : {ligne}")

#     sql = f"UPDATE info SET {ligne} = ? WHERE id = ?"
#     cur.execute(sql, (info, id_perso))
#     con.commit()
#     return cur.rowcount
