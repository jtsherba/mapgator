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
import chroma from "chroma-js";
import { latLngBounds } from "leaflet";
import * as turf from '@turf/turf'
export default {
  name: "Example",
  props: {name:Object, resultsData:Object, selectedAttribute:String},
  watch: {
    selectedAttribute(val){
        this.attribute = val
    }, 
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

      this.geojson.features.forEach(feature => {
        console.log(feature)
        console.log(this.attribute)
        let feature_id = feature.properties[this.attribute]
       
        feature.properties["data_value"] = val[feature_id].sample_data

      
      });
    
    this.geojson.features.splice(0, 0)
    
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
      attribute:null,
      fillColor: "#e4ce7f",
      classBreaks: [1,50,100,250,500,1000,2000,3000,6000,9000],
      colorHex: ['#deebf7','#08306b'],
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
    
  getColor(n) {
    var mapScale = chroma.scale(this.colorHex).classes(this.classBreaks);
    console.log(n)
    let regionColor = '#ffffff';
    if (n === 0) {
        regionColor = '#ffffff';
    } else { 
        regionColor = mapScale(n).hex();
    }
    return regionColor
    },
    styleFunction(feature) {
      let fillColor = '#08306b'
      if (feature.geojson === null){
        fillColor = '#08306b'
      }else{
        fillColor = this.getColor(feature.properties.data_value); // important! need touch fillColor in computed for re-calculate when change fillColor
      }
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
        console.log(feature)
        console.log(layer)
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
