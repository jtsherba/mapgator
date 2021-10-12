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
                      accept=".zip"
                      placeholder="Pick an zipped shapefile"
                      prepend-icon="mdi-map"
                      label="Shapefile"
                      v-model="chosenFile"
                      @change="onAddFiles"
                    ></v-file-input>
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

          <v-col>
            <v-sheet
              min-height="70vh"
              rounded="lg"
            >
              <LeafletMap :name="geojson"
              > </LeafletMap> 
               
            </v-sheet>
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
    }),
  methods:{
    onAddFiles() {
      //for the shapefiles in the files folder called pandr.shp
         
          let reader = new FileReader()
          reader.readAsArrayBuffer(this.chosenFile)
          reader.onload = () => {
            this.data = reader.result;
             shp(this.data).then((geojson) => {
            console.log(geojson)
            //see bellow for whats here this internally call shp.parseZip()
            this.geojson=geojson
            });
          }
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
    async runSummary(){
      const response = await fetch("https://api.census.gov/data/2019/acs/acs5/variables.json");
      let data = await response.json();
      //let censusVariable = data["variables"]
       const path = 'http://localhost:5000/ping';
      axios.get(path)
        .then((res) => {
          this.msg = res.data;
          console.log(this.msg)
          console.log(data)
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
         }, 

    
       }
    }
</script>
