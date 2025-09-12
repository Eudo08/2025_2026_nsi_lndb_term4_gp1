import sqlite3
con = sqlite3.connect("info_idividu.db")
cur = con.cursor()

cur.execute("CHARACTER SET utf8mb4")
cur.execute("COLLATE utf8mb4_general_ci;")

cur.execute("CREATE TABLE information (nom, prenom, pseudo, mot_passe, nb_personne, jour, heure)")

cur.execute("""
    INSERT INTO information VALUES
        (Eudocie, ABC, ABC, 123, 3, jeudi, 12h),
        (Arrivée, Tristan, flash, 456, 2, mercredi, 12h)
""")
con.commit()