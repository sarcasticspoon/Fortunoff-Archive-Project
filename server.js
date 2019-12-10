// Most of the authentication code is copied from the example provided from Shea Ketsdever
let express = require('express');
let sqlite3 = require('sqlite3').verbose();
let app = express();
const port = 8080;

// Serve up the original html and js files.
app.get('/',
  (req, res) => {
    res.sendFile(__dirname + "/index.html");
});

app.get('/js/index.js',
	(req, res) => {
	res.sendFile(__dirname + "/js/index.js");
});

app.get('/search',
	async function(req, res) {
        var rawData = [];
        let count = 0;
        let params = req.query;
        let lastInitial = "";
        let currTitle = "";

        if(params["last"].length > 1) {
            lastInitial = params["last"].substring(0, 1);
        }

        let db = new sqlite3.Database(__dirname + "/fortunoff.db");

        let sql = `SELECT DISTINCT title, path_index, latitude, longitude
                    FROM testimonies, agents, paths, places
                    WHERE testimonies.rowid = agents.id
                    AND testimonies.rowid = paths.id
                    AND paths.place_id = places.rowid
                    AND agents.first_name LIKE ?
                    AND agents.last_name LIKE ?
                    AND testimonies.rowid IN
                    (SELECT id FROM paths
                    WHERE place_id IN
                    (SELECT rowid FROM places
                    WHERE name LIKE ?))
                    ORDER BY testimonies.title ASC, paths.path_index ASC`;
        
        await db.all(sql, ["%" + params["first"] + "%", "%" + lastInitial + "%", "%" + params["place"] + "%"], (err, rows) => {
            if (err) {
                throw err;
            }
            rows.forEach((row) => {
                //console.log(currTitle);
                if(currTitle != row.title) {
                    count = rawData.push([]) - 1;
                    //console.log(count);
                    currTitle = row.title;
                    rawData[count].push(row.title);
                    //console.log(rawData);
                }
                else {
                    rawData[count].push([row.latitude, row.longitude]);
                    //console.log(rawData);
                }
            });

            res.setHeader('Content-Type', 'application/json');
            res.end(JSON.stringify(rawData));
        });
});

app.listen(port);