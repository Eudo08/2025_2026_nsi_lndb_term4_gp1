import sqlite3

con = sqlite3.connect("info_idividu.db")
cur = con.cursor()

# Fonction pour afficher proprement une table
def show_table(name):
    print(f"\n--- TABLE {name.upper()} ---")
    try:
        cur.execute(f"PRAGMA table_info({name})")
        columns = [col[1] for col in cur.fetchall()]
        print(" | ".join(columns))
        print("-" * 40)

        for row in cur.execute(f"SELECT * FROM {name}"):
            print(" | ".join(str(x) for x in row))

    except Exception as e:
        print(f"Erreur : {e}")


show_table("information")
show_table("planning")
show_table("association")

con.close()
