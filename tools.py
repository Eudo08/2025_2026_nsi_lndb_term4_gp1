import sqlite3
con = sqlite3.connect("info_idividu.db",check_same_thread=False)
cur = con.cursor()

def compar_infos_dej (nb_pers_voulu, jour_voulu, heure_voulu):
    cur.execute("SELECT nb_personne, jour, heure FROM information")
    if nb_pers_voulu == "nb_personne" and jour_voulu == "jour" and heure_voulu =="heure":
        return True
    else : 
        return False