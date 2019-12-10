let url = new URL('http://localhost:8080/search');
let params = {};
params["first"] = "";
params["last"] = "";
params["place"] = "United";

Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));

fetchResults(url);

async function fetchResults(searchUrl) {
	let result = await fetch(searchUrl);
	let rawData = await result.json();
	console.log(rawData);
}