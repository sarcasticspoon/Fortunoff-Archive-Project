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
    loadModules(['esri/Map', 'esri/views/MapView', 'esri/layers/GraphicsLayer', 'esri/Graphic', 'esri/layers/FeatureLayer'], { css: true })
    .then(([ArcGISMap, MapView, FeatureLayer]) => {
        let fLayer = new FeatureLayer();
        // this.getPaths();

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

        let map = new ArcGISMap({
            basemap: 'dark-gray-vector'
         });

        // map.basemap = 'topo-vector';

        // // let fLayer = new FeatureLayer();

        // let gLayer = new GraphicLayer();
     
        map.add(fLayer);
        
      this.view = new MapView({
        container: this.$el,
        map: map,
        center: [-118, 34],
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