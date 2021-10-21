<template>
  <v-app id="inspire">
    <v-app-bar
      app
      color="white"
      flat
    >
      <v-container class="py-0 fill-height">
        <v-avatar
          class="mr-10"
          color="grey darken-1"
          size="32"
        ></v-avatar>

        <v-btn
          v-for="link in links"
          :key="link"
          text
        >
          {{ link }}
        </v-btn>

        <v-spacer></v-spacer>

        
      </v-container>
    </v-app-bar>

    <v-main class="grey lighten-3">
      <v-container>
        <v-row>
          <v-col cols="4">
            <v-sheet rounded="lg">
              <v-list color="transparent">
                <v-list-item
                  link
                  color="grey lighten-4"
                >
                  <v-list-item-content>
                    <v-list-item-title>
                      Add a boundary shapefile
                    </v-list-item-title>
                      <v-file-input
                      show-size
                      :rules="rules"
                      accept=".zip,.geojson"
                      placeholder="Pick an zipped shapefile"
                      prepend-icon="mdi-map"
                      label="Shapefile"
                      v-model="chosenFile"
                      @change="onAddFiles"
                    ></v-file-input>
                  </v-list-item-content>
                </v-list-item>

                 <v-list-item
                  link
                  color="grey lighten-4"
                >
                  <v-list-item-content>
                    <v-list-item-title>
                      Select summary attribute
                    </v-list-item-title>
                   
                      <v-select
                        v-model="selectedAttribute"
                        :items="attributes"
                        label="Summary Attribute"
                        outlined
                      ></v-select>
                   
                  </v-list-item-content>
                </v-list-item>
                <v-divider class="my-2"></v-divider>
                <v-list-item
                  link
                  color="grey lighten-4"
                >
                  <v-list-item-content>
                    <v-list-item-title>
                      Select Census Group
                    </v-list-item-title>
                   
                      <v-select
                        v-model="selectedCensusGroup"
                        :items="censusGroups"
                        label="Census Groups"
                        outlined
                      ></v-select>
                   
                  </v-list-item-content>
                </v-list-item>
                <v-list-item
                  link
                  color="grey lighten-4"
                >
                  <v-list-item-content>
                    <v-list-item-title>
                      Select Census Attribute
                    </v-list-item-title>
                   
                      <v-select
                        v-model="selectedCensusAttribute"
                        :items="censusAttributes"
                        label="Census Attribute"
                        outlined
                      ></v-select>
                   
                  </v-list-item-content>
                </v-list-item>

                <v-divider class="my-2"></v-divider>

                <v-list-item
                  link
                  color="grey lighten-4"
                >
                  <v-list-item-content>
                      <div class="text-center">
                        <v-btn
                          class="ma-2"
                          :loading="loading"
                          :disabled="loading"
                          color="secondary"
                          @click="runSummary"
                        >
                          Get Data
                        </v-btn>
                         <v-btn
                          class="ma-2"
                          :loading="loading"
                          :disabled="loading"
                          color="secondary"
                          @click="loader = 'loading'"
                        >
                          Reset
                        </v-btn>
                       </div>
                  </v-list-item-content>
                </v-list-item>
              </v-list>
            </v-sheet>
          </v-col>

          <v-col cols = "6">
            <v-sheet
              min-height="70vh"
              rounded="lg"
            >
              <LeafletMap :name="geojson" :resultsData="resultsData" :selectedAttribute="selectedAttribute"
              > </LeafletMap> 
               
            </v-sheet>
          </v-col>
          <v-col cols="2" v-if= "showResults">
               <v-card
              
              max-width="344"
              outlined
            >
              <v-list-item three-line>
                <v-list-item-content>
                  <div class="text-overline mb-4">
                    OVERLINE
                  </div>
                  <v-list-item-title class="text-h5 mb-1">
                    Headline 5
                  </v-list-item-title>
                  <v-list-item-subtitle>Greyhound divisely hello coldly fonwderfully</v-list-item-subtitle>
                </v-list-item-content>

                <v-list-item-avatar
                  tile
                  size="80"
                  color="grey"
                ></v-list-item-avatar>
              </v-list-item>

              <v-card-actions>
                <v-btn
                  outlined
                  rounded
                  text
                >
                  Button
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
  import axios from 'axios';
  import shp from 'shpjs';
  import LeafletMap from './components/LeafletMap';
  import * as turf from '@turf/turf'
  export default {
    name: 'app',
    components: {
    LeafletMap
    },
    data: () => ({
      rules: [
        value => !value || value.size < 2000000000 || 'File size should be less than 2 MB!',
      ],
      links: [
        'Profile',
        'Updates',
      ],
      geojson:null,
      chosenFile: null,
      msg:null,
      tigerPolygons:null,
      intersections:[],
      loading:false, 
      showResults:true,
      resultsData:null, 
      attributes:[],
      selectedAttribute:null,
      selectedCensusAttribute: null,
      censusAttributes:[],
      selectedCensusGroup: null,
      censusGroups:[],
      groupLookup:null,
    }),
  mounted(){
      this.populateCensusDropdowns()
  },
  methods:{
    populateCensusDropdowns(){
      const censusGroupPath = 'https://api.census.gov/data/2019/acs/acs5/groups.json';
      axios.get(censusGroupPath)
        .then((res) => {
          console.log("test")
          console.log(res.data.groups)
          let allCensusVariables = []
          let allgroupLookup = {}
          res.data.groups.forEach((element) => { 
                allCensusVariables.push(element.description)
                allgroupLookup[element.description] = element.variables
          } )
          this.censusGroups =  allCensusVariables
          this.selectedCensusGroup = allCensusVariables[0]
          this.groupLookup = allgroupLookup
          

          axios.get(this.groupLookup[this.selectedCensusGroup])
              .then((res) => {
               console.log(res)
                
                
              })
              .catch((error) => {
                // eslint-disable-next-line
                console.error(error);
              });
          
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
       
    },
    onAddFiles() {
      //for the shapefiles in the files folder called pandr.shp
      if (this.chosenFile == null){
        return
      }else if(this.chosenFile.name.endsWith(".geojson")){
          console.log(this.chosenFile)
        let reader = new FileReader()
         reader.readAsText(this.chosenFile)
          reader.onload = () => {
            this.geojson = JSON.parse(reader.result);           
            this.updateAttributeSelection()
          }

            //Read the file as text.
  
      }else{
          console.log(this.chosenFile)
          let reader = new FileReader()
          reader.readAsArrayBuffer(this.chosenFile)
          reader.onload = () => {
            this.data = reader.result;
             shp(this.data).then((geojson) => {
            //see bellow for whats here this internally call shp.parseZip()
            this.geojson=geojson
            
            this.updateAttributeSelection()
            });
          }
      }
     },
    updateAttributeSelection(){
      console.log("test")
      console.log(this.geojson.features[0].properties)
       this.attributes = Object.keys(this.geojson.features[0].properties)
       this.selectedAttribute = this.attributes[0]
    }, 
    getMessage() {
      const path = 'http://localhost:5000/ping';
      axios.get(path)
        .then((res) => {
          this.msg = res.data;
          console.log(this.msg)
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getTigerPolygons() {
      let bbox = turf.bbox(this.geojson);
      console.log(bbox)
      const tigerPath = 'https://tigerweb.geo.census.gov/arcgis/rest/services/Generalized_ACS2019/Tracts_Blocks/MapServer/3/query?where=&text=&objectIds=&time=&geometry=-123.17382500000001%2C+37.639829999999996%2C+-122.28178%2C+37.929823999999996&geometryType=esriGeometryEnvelope&inSR=4269&spatialRel=esriSpatialRelIntersects&distance=&units=esriSRUnit_Foot&relationParam=&outFields=&returnGeometry=true&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=&havingClause=&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&historicMoment=&returnDistinctValues=false&resultOffset=&resultRecordCount=&returnExtentOnly=false&datumTransformation=&parameterValues=&rangeValues=&quantizationParameters=&featureEncoding=esriDefault&f=geojson';
      axios.get(tigerPath)
        .then((res) => {
          console.log("test")
          this.tigerPolygons = res.data;
          this.calculatePercentOverlay()
          
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
      
      //const response = await fetch("https://tigerweb.geo.census.gov/arcgis/rest/services/Generalized_ACS2019/Tracts_Blocks/MapServer/3/query");
      //this.tigerPolygons = await response.json();
      //console.log(this.tigerPolygons)
    },
    getACSVariable(){
      //const response = await fetch("https://api.census.gov/data/2019/acs/acs5/variables.json");
      //let data = await response.json();
      //let censusVariable = data["variables"]["B01001A_001E"]
    },
    calculatePercentOverlay(){
      for (const element of this.tigerPolygons.features) {

           for (const element2 of this.geojson.features) {
            var intersection = turf.intersect(element, element2);
            if (intersection != null){
            var polyAPolyBIntersectionPolyAIntersection = turf.intersect(intersection, element2);
            var polyAArea = turf.area(element2);
            var polyAPolyBIntersectionPolyAIntersectionArea = turf.area(polyAPolyBIntersectionPolyAIntersection);
            console.log(polyAArea)
            console.log(polyAPolyBIntersectionPolyAIntersectionArea)
// Calculate how much of polyA is covered.

            //var polyACoverage = polyAPolyBIntersectionPolyAIntersectionArea / polyAArea;
            }
           
             
              //this.intersections.push(polyACoverage)
              
        }
        }
       

      
      
      
    },
    async runSummary(){
      
      //this.getTigerPolygons()
      let bbox = turf.bbox(this.geojson);
      const path = 'http://localhost:5000/basicAnalysis';
      let payload = {'census_variables':["B01001A_001E"], "layer": this.geojson, "bbox":bbox, "summary_attribute": this.selectedAttribute}
      axios.post(path, payload)
        .then((res) => {
           console.log(res)
           this.resultsData = res.data.data

        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
         
        });
         }, 

    
       }
    }
</script>
