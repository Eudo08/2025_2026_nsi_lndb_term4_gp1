import sqlite3
import data

con = sqlite3.connect("info_idividu.db")
cur = con.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS information (
        nom TEXT,
        prenom TEXT,
        pseudo TEXT,
        mot_passe TEXT,
        nb_personne TEXT,
        jour TEXT,
        heure TEXT
    )
""")

cur.execute("""
    INSERT INTO information VALUES
        ('Eudocie', 'ABC', 'ABC', '123', '3', 'jeudi', '12h'),
        ('Arrivée', 'Tristan', 'flash', '456', '2', 'mercredi', '12h')
""")

cur.executemany("INSERT INTO information VALUES(?, ?, ?, ?, ?, ?)", data)



con.commit()