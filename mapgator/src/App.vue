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
         <v-snackbar
                v-model="snackbar"
                :timeout="timeout"
                absolute
                bottom
                color="primary"
                left
                text
              >
                {{ text }}

                <template v-slot:action="{ attrs }">
                  <v-btn
                    color="blue"
                    text
                    v-bind="attrs"
                    @click="snackbar = false"
                  >
                    Close
                  </v-btn>
                </template>
              </v-snackbar>
        <v-tabs
          v-model="tab"
          align-with-title
        >
          <v-tabs-slider color="yellow"></v-tabs-slider>

        <!--  <v-tab
            v-for="item in items"
            :key="item"
            
          >
            {{ item }}
          </v-tab>-->

          <v-tab
           
            :key="Analysis"
            
          >
            {{ "Analysis" }}
          </v-tab>
          <v-tab
            v-show="showResultsTab"
            :key="Results"
            
          >
            {{ "Results" }}
          </v-tab>
    </v-tabs>
  
  <v-tabs-items v-model="tab">
      <v-tab-item :key="analysis">
        <v-row>
          <v-col cols="8">
            <v-sheet rounded="lg">
              <v-form
                ref="form"
                v-model="valid"
                lazy-validation
              >
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
                      :rules="rulesUpload"
                      accept=".zip,.geojson"
                      placeholder="Pick an zipped shapefile"
                      prepend-icon="mdi-map"
                      label="Shapefile"
                      v-model="chosenFile"
                      @change="onAddFiles"
                      required
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
                        :rules="rules"
                        required
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
                        @change="onChangeGroup($event)"
                        outlined
                        :rules="rules"
                        required
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
                        :rules="rules"
                        outlined
                        required
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
              </v-form>
            </v-sheet>
          </v-col>

          <v-col cols = "4">
            <v-sheet
              min-height="70vh"
              rounded="lg"
            >
              <LeafletMap :name="geojson" :resultsData="resultsData" :selectedAttribute="selectedAttribute"
              > </LeafletMap> 
               
            </v-sheet>
          </v-col>
         
        </v-row>
         </v-tab-item>
          <v-tab-item :key="results">
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
          </v-tab-item> 
        </v-tabs-items>
        
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
        v => !!v || 'Name is required'
      ],
     rulesUpload: [
        v => !!v || 'File is required',
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
      variableIDLookup:null,
      tab: null,
      items: [
          "Analysis", "Results"
        ],
      analysis:"analysis",
      results:"results",
      showResultsTab:false,
      valid: false,
      snackbar: false,
      text: 'Required inputs missing.',
      timeout: 2000,
    }),
  mounted(){
      this.populateCensusDropdowns()
  },
  methods:{
    onChangeGroup() {
            //console.log(event.target.value)
            axios.get(this.groupLookup[this.selectedCensusGroup])
              .then((res) => {
               let variableIDLookupAll = {}
               let variableLabels = []
               Object.entries(res.data.variables).forEach((element) => { 
                if (element[0].endsWith("E") && ! element[0].endsWith("PE")){
                  variableLabels.push(element[1].label)
                  variableIDLookupAll[element[1].label] = element[0]
                }
                } )
                this.censusAttributes = variableLabels.sort()
                this.selectedCensusAttribute = variableLabels[0]
                
                this.variableIDLookup = variableIDLookupAll
                
              })
              .catch((error) => {
                // eslint-disable-next-line
                console.error(error);
              });
     },
    populateCensusDropdowns(){
      //const censusGroupPath = 'https://api.census.gov/data/2019/acs/acs5/groups.json';
      const censusGroupPath = 'https://api.census.gov/data/2019/acs/acs5/profile/groups.json';
      axios.get(censusGroupPath)
        .then((res) => {
         
          let allCensusGroupVariables = []
          let allgroupLookup = {}
          res.data.groups.forEach((element) => { 
                allCensusGroupVariables.push(element.description)
                allgroupLookup[element.description] = element.variables
          } )
          this.censusGroups =  allCensusGroupVariables
          this.selectedCensusGroup = allCensusGroupVariables[0]
          this.groupLookup = allgroupLookup
          

          axios.get(this.groupLookup[this.selectedCensusGroup])
              .then((res) => {
              
               let variableIDLookupAll = {}
               let variableLabels = []
               Object.entries(res.data.variables).forEach((element) => { 
                if (element[0].endsWith("E") && ! element[0].endsWith("PE")){
                  variableLabels.push(element[1].label)
                  variableIDLookupAll[element[1].label] = element[0]
                }
                } )
                this.censusAttributes = variableLabels.sort()
                this.selectedCensusAttribute = variableLabels[0]
                
                this.variableIDLookup = variableIDLookupAll
                
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
        this.geojson = {"empty":"true"}
        this.attributes = []
        return
      }else if(this.chosenFile.name.endsWith(".geojson")){
      
        let reader = new FileReader()
         reader.readAsText(this.chosenFile)
          reader.onload = () => {
            this.geojson = JSON.parse(reader.result);           
            this.updateAttributeSelection()
          }

            //Read the file as text.
  
      }else{
          
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
       this.attributes = Object.keys(this.geojson.features[0].properties)
       this.selectedAttribute = this.attributes[0]
    }, 
   /* getMessage() {
      const path = 'http://localhost:5000/ping';
      axios.get(path)
        .then((res) => {
          this.msg = res.data;
          
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getTigerPolygons() {
      //let bbox = turf.bbox(this.geojson);
   
      const tigerPath = 'https://tigerweb.geo.census.gov/arcgis/rest/services/Generalized_ACS2019/Tracts_Blocks/MapServer/3/query?where=&text=&objectIds=&time=&geometry=-123.17382500000001%2C+37.639829999999996%2C+-122.28178%2C+37.929823999999996&geometryType=esriGeometryEnvelope&inSR=4269&spatialRel=esriSpatialRelIntersects&distance=&units=esriSRUnit_Foot&relationParam=&outFields=&returnGeometry=true&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=&havingClause=&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&historicMoment=&returnDistinctValues=false&resultOffset=&resultRecordCount=&returnExtentOnly=false&datumTransformation=&parameterValues=&rangeValues=&quantizationParameters=&featureEncoding=esriDefault&f=geojson';
      axios.get(tigerPath)
        .then((res) => {
         
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
    },*/

    runSummary(){

      
      if (this.$refs.form.validate() === true){
        console.log(this.valid)
      this.loading = true
      //this.tab = 1
      //this.getTigerPolygons()
      let bbox = turf.bbox(this.geojson);
      this.selectedCensusAttribute
      
      let singleCensusVariable = this.variableIDLookup[this.selectedCensusAttribute]
      const path = 'http://localhost:5000/basicAnalysis';
      let payload = {'census_variables':[singleCensusVariable], "layer": this.geojson, "bbox":bbox, "summary_attribute": this.selectedAttribute}
      console.log(payload)
      axios.post(path, payload)
        .then((res) => {
        
           this.resultsData = res.data.data
           this.loading = false
           this.showResultsTab =true
           this.tab = 1

        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
         
        });
      }else{
         this.snackbar = true
      }
         }, 

    
       }
    }
</script>
