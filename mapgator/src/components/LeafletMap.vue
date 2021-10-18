<template>

  <div>
    <div>
      <span v-if="loading">Loading...</span>
      
    </div>
    <l-map
      :zoom="zoom"
      
      :bounds="bounds"  
      style="height: 500px; width: 100%"
    >
      <l-tile-layer
        :url="url"
        :attribution="attribution"
      />
      <l-geo-json
        v-if="show"
        :geojson="geojson"
        :options="options"
        :options-style="styleFunction"
      />
    </l-map>
  </div>
</template>

<script>
import { LMap, LTileLayer, LGeoJson } from "vue2-leaflet";
import { latLngBounds } from "leaflet";
import * as turf from '@turf/turf'
export default {
  name: "Example",
  props: {name:Object, resultsData:Object},
  watch: {
    name(val) {
      this.loading = true;
      this.geojson = JSON.parse(JSON.stringify(val));
      let bbox = turf.bbox(this.geojson);
      let latlngbbox = latLngBounds([
        [bbox[1], bbox[0]],
        [bbox[3], bbox[2]]
      ])
      this.bounds=latlngbbox
      this.loading = false;
    }, 
    resultsData(val){

      console.log(val)
      console.log(this.geojson)
    }
  },  
  components: {
    LMap,
    LTileLayer,
    LGeoJson,
  },
  data() {
    return {
      loading: false,
      show: true,
      enableTooltip: true,
      zoom: 6,
      //center: [38, -122.2],
      bounds: latLngBounds([
        [49, -66],
        [25, -124]
      ]),
      geojson: null,
      fillColor: "#e4ce7f",
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      attribution:
        '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
     
    };
  },
  computed: {
    options() {
      return {
        onEachFeature: this.onEachFeatureFunction
      };
    },
    styleFunction() {
      const fillColor = this.fillColor; // important! need touch fillColor in computed for re-calculate when change fillColor
      return () => {
        return {
          weight: 2,
          color: "#ECEFF1",
          opacity: 1,
          fillColor: fillColor,
          fillOpacity: 1
        };
      };
    },
    onEachFeatureFunction() {
      if (!this.enableTooltip) {
        return () => {};
      }
      return (feature, layer) => {
        let attributeHTML = ""
        for (const [key, value] of Object.entries(feature.properties)) {
          attributeHTML += "<div>"+ key + ": " + value + "</div>"
        }
        layer.bindTooltip(attributeHTML)
      };
    }
  },
  async created() {
    //this.loading = true;
    //const response = await fetch("https://rawgit.com/gregoiredavid/france-geojson/master/regions/pays-de-la-loire/communes-pays-de-la-loire.geojson")
    //const data = await response.json();
    //console.log(data)
    //this.geojson = data;
    //this.loading = false;
  }
};
</script>
