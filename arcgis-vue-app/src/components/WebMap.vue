<template>
    <div>
        <div style="padding-left:100px;">
        <b-navbar>
            <b-nav-form inline class="ml-auto" style="padding-right:5px;">
              <b-form-input v-model="searchTerms.placename" placeholder = "Place" > </b-form-input>
              <!-- <b-form-input placeholder ="Ellie"> </b-form-input> -->
              <b-form-input v-model="searchTerms.firstname" placeholder = "FirstName"> </b-form-input> 
              <b-form-input v-model="searchTerms.lastname" placeholder = "LastName"> </b-form-input> 
              <b-button variant = "outline-dark" @click="searchPaths"> Search </b-button>
              <b-button variant = "outline-dark" @click="resetPaths"> Reset </b-button>
          </b-nav-form>
        </b-navbar>
        </div>
    </div>

</template>

<script>
import ArcGISMap from 'esri/Map';
import MapView from 'esri/views/MapView';
import GraphicsLayer from 'esri/layers/GraphicsLayer';
import FeatureLayer from 'esri/layers/FeatureLayer';

export default {
    name: 'MappyBoy',
    props: {
    },
    data: () => ({
        graphicsArray: [],
        graphic : FeatureLayer,
        cities : FeatureLayer,
        testerString: '',
        searchTerms : {
            placename: '',
            firstname: '',
            lastname: ''
        },
        testNumber : 0
    }),
    methods: {
        searchPaths: async function() {
            // console.log(this.searchTerms);
            await this.makeGraphics(this.searchTerms);
            this.view.map.layers = this.graphic;
        }, 
        resetPaths : async function() {
            let empty = {
                placename: "",
                lastname: "",
                firstname: ""
            }
            await this.makeGraphics(empty);
            this.view.map.layers = this.graphic;
        },
        fetchPathData : async function(searchTerms) {
            let url = new URL('http://localhost:3000/search');
            let params = {};
            params["first"] = searchTerms.firstname;
            params["last"] = searchTerms.lastname;
            params["place"] = searchTerms.placename;
            // params["first"] = "";
            // params["last"] = "";
            // params["place"] = "";

            Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));

            console.log(url);

            let result = await fetch(url, {
                headers : {
                    'Content-Type' : 'application/json',
                    'Accept' : 'application/json',
                    'credentials' : 'include',
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Credentials": "true",
                    "Access-Control-Allow-Methods": "GET,HEAD,OPTIONS,POST,PUT",
                    "Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept"
                }
            });
            let rawData = await result.json();
            this.testerString = rawData[0][0];
            console.log(rawData);
            return rawData;
        }, 
        addCityData : function() {
            let city1 = {
                title: "Auschwitz",
                coordinates: [19.2214053, 50.0382443],
                description : "The Auschwitz concentration camp was a complex of over 40 concentration and extermination camps built and operated by Nazi Germany in occupied Poland during World War II and the Holocaust. \nLearn more from the Holocaust Encylcopedia <a target='blank' window.location.href = 'https://www.google.com'; >here</a>"
            }

            let city2 = {
                title: "Warsaw",
                coordinates: [21.0067265, 52.2319237],
                description: "Warsaw is the capital and largest city of Poland. \n Learn more from the Holocaust Encylcopedia <a href=”https://encyclopedia.ushmm.org/content/en/article/warsaw”>here</a>"
            }

            let city3 = {
                title : "Plaszow",
                coordinates: [19.9946003, 50.0401685],
                description: "The Płaszów camp was established in 1942 under the authority of the SS and police leaders in Krakow (Cracow). It was initially a forced-labor camp for Jews.  \n Learn more from the Holocaust Encylcopedia <a href=”https://encyclopedia.ushmm.org/content/en/article/plaszow”>here</a>"
            }

            let city4 = {
                title : "Mauthausen",
                coordinates : [14.5164058, 48.2403315],
                description : "The Mauthausen–Gusen concentration camp complex consisted of the Mauthausen concentration camp on a hill above the market town of Mauthausen plus a group of nearly 100 further subcamps located throughout Austria and southern Germany. \n Learn more from the Holocaust Encylcopedia <a href=”https://encyclopedia.ushmm.org/content/en/article/mauthausen”>here</a>"
            }

            let cityArray = [city1, city2, city3, city4];

            let features = [];

            let i;
            let sym = {
                type : "simple-marker",
                color: "#d3d3d3",
                size : "10px"
            };
            for(i = 0; i < cityArray.length; i++) {
                let point = {
                    type: "point",
                    longitude: cityArray[i].coordinates[0],
                    latitude: cityArray[i].coordinates[1]
                };

                let pointGraphic = {
                    geometry: point,
                    symbol: sym,
                    attributes : {
                        cityName : cityArray[i].title,
                        description : cityArray[i].description,
                        cityID : i
                    }
                };

            features.push(pointGraphic);

            }

            let cityPopup = {
                title : "{cityName}",
                content : "{description}"
            };

            let renderer = {
                type: "simple",
                symbol: sym
            }

            let fLayer = new FeatureLayer({
                source : features,
                objectIdField : "cityID",
                fields : [
                    { name: "cityName",
                        type: "string"
                    }, 
                    { name: "description",
                    type: "string"
                    },
                    {
                        name: "cityID",
                        type : "number"
                    }
                ],
                renderer: renderer,
                geometryType: "point",
                popupTemplate: cityPopup
            });

            this.cities = fLayer;

        },

        makeGraphics : async function(searchTerms) {

            // use the JSON object to make a feature layer
            let features = [];

            let obj = await this.fetchPathData(searchTerms);

            console.log(obj);
            let i;
            for(i = 0; i < obj.length; i++) {
                let sym = {
                    type: "simple-line",
                    color: [255 * Math.random(), 255 * Math.random(), 255 * Math.random()],
                    width: 3
                };

                let path = this.switchLatLon(obj[i]);
                
                // let path = [];
                // let j;
                // for(j = 1; j < obj[i].length; j++) {
                //     path.push(obj[i][j]);
                // }
                // let pattern = "/Holocaust testimony[.]+/";
                let name = obj[i][0];
                let splitName = name.split(" Holocaust");
                // console.log(splitName[0]);
                // console.log(pattern.test(obj[i][0]));

                let geo = {
                    symbol : sym,
                    geometry : {
                        type: "polyline",
                        paths: path
                    },
                    attributes : {
                        personName : splitName[0],
                        featureID : i,
                        summary : obj[i][1]
                    }
                }
                features.push(geo);
            }

            // console.log(features);
            let poppyBoy = {
                title : "{personName}",
                content : "{summary}"
            }

            let sym = {
                    type: "simple-line",
                    color: "#ca6151"
            };


            let rendyBoy = {
                type: "simple",
                symbol: sym
            }

            let fLayer = new FeatureLayer({
                source : features,
                objectIdField : "featureID",
                fields : [
                    { name: "personName",
                        type: "string"
                    }, {
                        name: "featureID",
                        type: "number"
                    },
                    {
                        name: "summary",
                        type: "string"
                    }
                ],
                renderer: rendyBoy,
                geometryType: "polyline",
                popupTemplate: poppyBoy
            });

            this.graphic = fLayer;

        },
        fetchResults : async function (url) {
            let result = await fetch(url);
            let rawData = await result.json();
            return rawData;
        },
        switchLatLon : function (mixedPath) {
            let newPath = [];
            let i;
            for (i = 2; i < mixedPath.length; i++) {
                newPath.push([mixedPath[i][1], mixedPath[i][0]]);
            }

            return newPath;
        }
    },
    mounted: async function () {
        const map = new ArcGISMap({
            basemap: 'dark-gray-vector'
        });

        let empty = {
            placename: "",
            firstname: "",
            lastname: ""
        }
        // this.getPaths();
        await this.makeGraphics(empty);
        this.addCityData();
        console.log(this.graphic);
        console.log(this.cities);
        // this.getPaths();
        let tester = new FeatureLayer();
        tester = this.graphic;
        
        // map.add(gLayer);
        map.add(tester);
        map.add(this.cities);
        
        this.view = new MapView({
            container: this.$el,
            map: map,
            center: [-4.046413, 41.812756],
            zoom: 3
        });
    },
    beforeDestroy() {
      // destroy the map view
      if (this.view) {
        this.view.container = null;
      }
    }
};
</script>

<style lang="scss" scoped>
div {
    padding: 0;
    margin: 0;
    width: 100%;
    height: 100%;
}

h1 {
    color : "#1099ab"
}
</style>