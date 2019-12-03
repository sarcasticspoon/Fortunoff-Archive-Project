import sqlite3

with sqlite3.connect("fortunoff.db") as con:
    cur = con.cursor()
    cur.execute("DELETE FROM testimonies")
    cur.execute("DELETE FROM agents")
    cur.execute("DELETE FROM entities")
    cur.execute("DELETE FROM places")
    cur.execute("DELETE FROM subjects")
    cur.execute("DELETE FROM paths")
    con.commit()