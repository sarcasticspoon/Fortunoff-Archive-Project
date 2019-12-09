// Most of the authentication code is copied from the example provided from Shea Ketsdever
let express = require('express');
let proxy = require('express-http-proxy');
let app = express();
let fetch = require('cross-fetch');
let passport = require('passport');
let GitHubStrategy = require('passport-github').Strategy;
let { URL } = require('url');
let port = 3000;
let apikey = "9b6de350-d8ae-11e9-9306-1db72f950177";
let harvardURL = "https://api.harvardartmuseums.org/";
// Global variables for tracking session information
let sess;
let galIndex = 0;

// 1. PRIVATE KEYS
const GITHUB_CLIENT_ID = "35615ef1432db38a8c1e";
const GITHUB_CLIENT_SECRET = "8e15c701f1196c2a62149821ef25d82fbb62a4e4";

app.use('/vue', proxy('http://localhost:8080'));

// This is how Passport keeps track of user sessions / if a login has been successful.
app.use(require('express-session')({ secret: 'oranges', resave: true, saveUninitialized: true }));

// 3. PASSPORT
// Create github strategy
passport.use(new GitHubStrategy({
  clientID: GITHUB_CLIENT_ID,
  clientSecret: GITHUB_CLIENT_SECRET,
  callbackURL: "http://localhost:3000/auth/github/callback"  // update URL if you don't use localhost
},
function(accessToken, refreshToken, profile, cb) {
  return cb(null, profile);
}
));

// Configure authenticated session persistence. 
passport.serializeUser(function(user, cb) {
  cb(null, user);
});
passport.deserializeUser(function(obj, cb) {
  cb(null, obj);
});

// Initialize and restore authentication state, if any, from the session. This will create a
// new session every time the server is restarted -- so note that you have to restart the
// server for it to detect logouts on an external website (eg. github).ยตยต
//
// These two lines must come AFTER your call to require('express-session')
app.use(passport.initialize());
app.use(passport.session());

// Serve up the original html and js files.
app.get('/',
  require('connect-ensure-login').ensureLoggedIn(), // this is how you require authentication on a route
  (req, res) => {
  	// Initialize a list of the most recent gallery expansions, if it doesn't already exist
  	sess = req.session;
  	if(!sess.galleries) {
  		sess.galleries = [0, 0, 0, 0, 0];
  	}
    res.redirect('/vue/');
  });

app.get('/js/index.js',
	require('connect-ensure-login').ensureLoggedIn(),
	(req, res) => {
	res.sendFile(__dirname + "/js/index.js");
});

// Set up the login callbacks.
app.get('/login',
  passport.authenticate('github'));

app.get('/auth/github/callback', 
  passport.authenticate('github', { failureRedirect: '/login' }),
  function(req, res) {
    res.redirect('/vue/');
});

app.get('/gallery',
	require('connect-ensure-login').ensureLoggedIn(),
	function(req, res) {
		handleRequest(req, res, "gallery");
});

app.get('/object',
	require('connect-ensure-login').ensureLoggedIn(),
	function(req, res) {
		/*
		sess = req.session;
		params = req.query;
		// If this endpoint was accessed to expand a gallery, add the gallery ID to the session variable
		if(params.gallery) {
			let addToSess = true;
			// Prevent repeats
			sess.galleries.forEach(function(item) {
				if(item == params.gallery) {
					addToSess = false;
				}
			});
			if(addToSess) {
				sess.galleries[galIndex] = params.gallery;
				if(galIndex == 4) {
					galIndex = 0;
				} else {
					galIndex++;
				}
			}
		}
		*/
		handleRequest(req, res, "object");
});

app.get('/classification',
	require('connect-ensure-login').ensureLoggedIn(),
	function(req, res) {
		handleRequest(req, res, "classification");
});

app.get('/person',
	require('connect-ensure-login').ensureLoggedIn(),
	function(req, res) {
		handleRequest(req, res, "person");
});

app.get('/place',
	require('connect-ensure-login').ensureLoggedIn(),
	function(req, res) {
		handleRequest(req, res, "place");
});

app.get('/recent',
	require('connect-ensure-login').ensureLoggedIn(),
	function(req, res) {
		// Sends back the list of most recently expanded gallery ID's
		res.setHeader('Content-Type', 'application/json');
    	res.end(JSON.stringify(req.session.galleries));
});

// Processes the "next" url in the JSON response from the museum API to remove the API key
// and replace the harvard API museum url with this server url
function wipeKey(data) {
	let url = data.info.next;

	url = url.replace("https://api.harvardartmuseums.org", "http://localhost:3000");

	let apiPatt = /apikey=[^&]+&/;
	// Checks for API key at the end of the url
	let apiPattEnd = /&?apikey=[^&]+$/;
	url = url.replace(apiPatt, "");
	url = url.replace(apiPattEnd, "");
	data.info.next = url;
	return data;
}

// Takes the url coming from the client, adds the apikey and museum API url to it, and
// forwards it to the museum API
async function handleRequest(req, res, API) {
	let url = new URL(harvardURL + API);
	let params = req.query;
	params["apikey"] = apikey;
	params["size"] = "100";

	Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));
	let result = await fetch(url);
	let rawData = await result.json();

	// Process the "next" url if it exists
	if(rawData.info.next) {
		rawData = wipeKey(rawData);
	}

	// Send response back to client, in same exact format from the museum API, minus
	// the "next" url
	res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify(rawData));
}

app.listen(port);