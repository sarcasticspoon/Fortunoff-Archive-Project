import sqlite3, csv

with sqlite3.connect('fortunoff.db') as con:
    cur = con.cursor()

    with open('data/path_data.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            title = row[0].strip()
            path = row[2]
            # Don't forget usable code
            if not title == "title":
                cur.execute("SELECT rowid FROM testimonies WHERE title=?", [title])
                rowid = cur.fetchone()[0]
                placeid = ""
                count = 0

                for place in path:
                    cur.execute("INSERT OR IGNORE INTO places (city) VALUES (?)", [place])
                    con.commit()

                    cur.execute("SELECT rowid FROM places WHERE city=?", [place])
                    placeid = cur.fetchone()[0]
                    cur.execute("INSERT INTO paths (id, path_index, place_id) VALUES (?,?,?)", [rowid, count, placeid])
                    con.commit()
                    
    cur.close()