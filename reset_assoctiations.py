import sqlite3

con = sqlite3.connect("info_idividu.db")
cur = con.cursor()

cur.execute("DELETE FROM association")
con.commit()

print("Table 'association' nettoyée ✔")

con.close()
