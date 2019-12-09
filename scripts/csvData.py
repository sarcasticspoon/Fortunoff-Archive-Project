from requests.models import PreparedRequest
import sqlite3, csv, json
import urllib.request as request

def convertCoords(dms):
    dms = dms.split(" ")
    dd = float(dms[0][:-1]) + float(dms[1][:-1])/60 + float(dms[2][:-2])/(60*60)
    if dms[3] == "W" or dms[3] == "S":
        dd *= -1
    return dd

with sqlite3.connect('fortunoff.db') as con:
    cur = con.cursor()
    count = 0

    with open('data/path_data.csv', 'r') as f:
        reader = csv.reader(f)
        placeSet = {}
        errors = open("errors.txt", "w+")

        for row in reader:
            title = row[0].strip()
            path = row[6].split("', '")
            if len(path[0]) > 2:
                path[0] = path[0][2:]
                pathLength = len(path)
                path[pathLength - 1] = path[pathLength - 1][:-2]
            else:
                break
            
            usable = 0
            if not row[7] == "usable":
                usable = int(row[7])
            
            if not title == "title" and usable == 1:
                cur.execute("SELECT rowid FROM testimonies WHERE title=?", [title])
                rowid = cur.fetchone()[0]
                placeid = ""
                count = 0

                for place in path:
                    if not place in placeSet:
                        req = PreparedRequest()
                        params = {'q' : place}
                        url = "https://api.opencagedata.com/geocode/v1/json?key=df01aa2ead3c489aaede3213e08ea0ce"

                        req.prepare_url(url, params)
                        latitude = 0
                        longitude = 0
                        with request.urlopen(req.url) as response:
                                if response.getcode() == 200:
                                    source = response.read()
                                    data = json.loads(source)
                                    if data['results'] and len(data['results']) >= 1:
                                        latitude = data['results'][0]['annotations']['DMS']['lat']
                                        longitude = data['results'][0]['annotations']['DMS']['lng']
                                    else:
                                        errors.write("'" + place + "', ")
                                else:
                                    errors.write("'" + place + "', ")

                        if not latitude == 0:
                            latitude = convertCoords(latitude)
                        if not longitude == 0:
                            longitude = convertCoords(longitude)
                        cur.execute("INSERT OR IGNORE INTO places (name, latitude, longitude) VALUES (?, ?, ?)", [place, latitude, longitude])
                        con.commit()

                    cur.execute("SELECT rowid FROM places WHERE name=?", [place])
                    placeid = cur.fetchone()[0]
                    cur.execute("INSERT INTO paths (id, path_index, place_id) VALUES (?,?,?)", [rowid, count, placeid])
                    con.commit()
                    count += 1
                    
        errors.close()

    cur.close()