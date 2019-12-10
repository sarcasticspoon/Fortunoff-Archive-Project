<template>
  <div></div>
</template>

<script>
import { loadModules } from 'esri-loader';
// import FeatureLayer from './components/FeatureLayer.vue';

export default {
  name: 'WebMap',
  data: () => ({ // its own internal variables
    graphicsArray : ''
  }),
  methods: {
      getPaths: async function () {
          loadModules(['esri/Graphic'], {css: true})
          .then((Graphic) => {
            let polyAtt = {
                Name: "tester123"
            };
            let simpleLineSymbol = {
                type: "simple-line",
                color: "red"
            };

            var paths2 = [];
                paths2.push([21.0122, 52.2297]);
                paths2.push([-0.1180, 51.510]);
                paths2.push([2.3522, 48.8566]);

            let polyline = {
                type : "polyline",
                paths: paths2
            };

            let polylineGraphic = new Graphic({
                geometry: polyline,
                symbol: simpleLineSymbol,
                attributes: polyAtt
            });

            this.graphicsArray = polylineGraphic;
          });
      }
  }, 
  mounted() {
    // lazy load the required ArcGIS API for JavaScript modules and CSS
    loadModules(['esri/Map', 'esri/views/MapView', 'esri/layers/GraphicsLayer', 'esri/Graphic', 'esri/layers/FeatureLayer'], {css: true})
    .then(([Map, MapView, GraphicsLayer, FeatureLayer]) => {
        // let features = [];
        let farArray = [];

        var paths2 = [];
        paths2.push([21.0122, 52.2297]);
        paths2.push([-0.1180, 51.510]);
        paths2.push([2.3522, 48.8566]); 

        // Random colors
        let red = 255 * Math.random();
        let green = 255 * Math.random();
        let blue = 255 * Math.random();

        let sym = {
            type: "simple-line", 
            color: [red, green, blue],
            width: 3,
        };

        // create individual line paths
        let geo = {
            symbol: sym,
            geometry: {
                type: "polyline",
                paths: paths2},
            attributes: {
                birthday: "December"
            }
        };

        let gLayer = new GraphicsLayer();
        gLayer.add(geo);

        var rendyBoy = {
            type: "simple",  // autocasts as new SimpleRenderer()
            symbol: sym
        };
    
        farArray.push(geo);
        const fLayer = new FeatureLayer({
            source: farArray,
            objectIdField: "birthday",
            fields: [ 
                {name: "birthday",
                type: "string" }
            ],
            renderer: rendyBoy,
            geometryType : "polyline"
        });

        let map = new Map({
            basemap: 'dark-gray-vector'
        });

        map.add(fLayer);
        map.add(gLayer);
        
      this.view = new MapView({
        container: this.$el,
        map: map,
        center: [21.0122, 52.2297],
        zoom: 8
      });
    });
  },
  beforeDestroy() {
    if (this.view) {
      // destroy the map view
      this.view.container = null;
    }
  }
};

</script>

<style scoped>
div {
  padding: 0;
  margin: 0;
  width: 100%;
  height: 100%;
}
</style>
