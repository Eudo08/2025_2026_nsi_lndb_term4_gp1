import sqlite3
# from data import infos_perso

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

# cur.execute("""
#     INSERT INTO information VALUES
#         ('Eudocie', 'ABC', 'ABC', '123', '3', 'jeudi', '12h'),
#         ('Arrivée', 'Tristan', 'flash', '456', '2', 'mercredi', '12h')
# """)

# data = [
#     ('Joe', 'Abc', 'Abc', '16287', '4', 'mardi', '13'),
#     ('Xenia', 'bdh', 'Aozsnbc', '7383', '4', 'mardi', '13')
# ]
def add_infos (prenom, nom, nom_utilisateur, mot_passe):
    cur.executemany("INSERT INTO information VALUES(prenom, nom, nom_utilisateur, mot_passe, ?, ?, ?)")


con.commit()
con.close()

