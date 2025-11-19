import sqlite3

con = sqlite3.connect("info_idividu.db")
cur = con.cursor()

print("\n--- TABLE information ---")
for row in cur.execute("SELECT * FROM information"):
    print(row)

print("\n--- TABLE planning ---")
for row in cur.execute("SELECT * FROM planning"):
    print(row)

con.close()
