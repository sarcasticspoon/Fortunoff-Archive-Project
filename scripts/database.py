from pymarc import MARCReader
import sqlite3, csv

with sqlite3.connect("fortunoff.db") as con:
    cur = con.cursor()

    cur.execute("CREATE TABLE testimonies(title TEXT, summary TEXT)")
    cur.execute("CREATE TABLE agents(id INTEGER, first_name TEXT, last_name TEXT, PRIMARY KEY (id, first_name, last_name)) WITHOUT ROWID")
    cur.execute("CREATE TABLE entities(id INTEGER, name TEXT, PRIMARY KEY (id, name)) WITHOUT ROWID")
    cur.execute("CREATE TABLE subjects(id INTEGER, name TEXT, PRIMARY KEY (id, name)) WITHOUT ROWID")
    cur.execute("CREATE TABLE places(name TEXT, latitude REAL, longitude REAL)")
    cur.execute("CREATE TABLE paths(id INTEGER, path_index INTEGER, place_id INTEGER, PRIMARY KEY (id, path_index)) WITHOUT ROWID")
    con.commit()

    with open('data/fortunoff.mrc', 'rb') as fh:
        reader = MARCReader(fh)
        for record in reader:
            title = record.title().strip()
            summ = ""
            for f in record.get_fields('520'):
                summ += f['a']

            alterStr = ""
            for x in summ:
                if x == '︠':
                    continue
                elif x == '︡':
                    continue
                else:
                    alterStr += x

            cur.execute("INSERT INTO testimonies (title, summary) VALUES (?, ?)", [title, alterStr])
            con.commit()
            cur.execute("SELECT rowid FROM testimonies WHERE title=?", [title])

            rowID = cur.fetchone()[0]

            names = []
            for f in record.get_fields('600'):
                name = f['a'].split(',')
                if len(name) <= 1:
                    name = f['a'].split(' ')
                if len(name) <= 1:
                    name.insert(0, "N/A")
                    
                name[0] = name[0].strip()
                name[1] = name[1].strip()
                cur.execute("INSERT OR IGNORE INTO agents (id, first_name, last_name) VALUES (?, ?, ?)", [rowID, name[1], name[0]])

            con.commit()

            for f in record.get_fields('610'):
                cur.execute("INSERT OR IGNORE INTO entities (id, name) VALUES (?, ?)", [rowID, f['a']])
            
            con.commit()

            for f in record.get_fields('650'):
                cur.execute("INSERT OR IGNORE INTO subjects (id, name) VALUES (?, ?)", [rowID, f['a']])
            for f in record.get_fields('690'):
                cur.execute("INSERT OR IGNORE INTO subjects (id, name) VALUES (?, ?)", [rowID, f['a']])

            con.commit()
    cur.close()