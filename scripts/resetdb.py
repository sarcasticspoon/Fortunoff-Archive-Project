import sqlite3, sys

with sqlite3.connect("fortunoff.db") as con:
    cur = con.cursor()
    if len(sys.argv) == 2 and sys.argv[1] == "full":
        cur.execute("DELETE FROM testimonies")
        cur.execute("DELETE FROM agents")
        cur.execute("DELETE FROM entities")
        cur.execute("DELETE FROM places")
        cur.execute("DELETE FROM subjects")
    cur.execute("DELETE FROM paths")
    con.commit()
    cur.close()