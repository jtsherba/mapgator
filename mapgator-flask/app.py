from flask import Flask, jsonify, request
from flask_cors import CORS

# base libraries
import requests, json, os
import pandas as pd
import numpy as np
from collections import defaultdict
import geopandas

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# sanity check route
@app.route('/basicAnalysis',  methods=['GET', 'POST'])
def process_request():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        run_basic_anlysis(post_data)
        
    
    return jsonify(response_object)


def run_basic_anlysis(post_data):
    attribute_ids = post_data["census_variables"]
    layer = post_data["layer"]
    df_layer = geopandas.GeoDataFrame.from_features(layer["features"])
    df_layer = df_layer.set_crs(4326, allow_override=True)
    df_layer= df_layer.to_crs({'init': 'epsg:3857'})
    df_layer["area_layer"] = df_layer['geometry'].area
    bbox = post_data["bbox"]
    # set geo variables for api call
    tract_code = "*"
    state_code = "06"
    county_code = "075"

    # split attributes into groups of 45, run a census query for each, merge outputs into a single df
    split_attribute_ids = [attribute_ids[i:i+45] for i in range(0, len(attribute_ids), 45)]
    df=None
    first = True
    for ids in split_attribute_ids:
        census_url = build_census_url(tract_code, state_code, county_code, ids)

        returned_df = make_census_api_call(census_url)
        if first:
            df = returned_df
            first = False
        else:
            returned_df = returned_df.drop(columns=['state', 'county'])
            df = pd.merge(df, returned_df, on=['tract'], how='left')

    
    tiger_df = make_tiger_api_call(bbox)
    tiger_df= tiger_df.to_crs({'init': 'epsg:3857'})
    #tiger_df = tiger_df.dropna()
    #df_layer = df_layer.dropna()
    tiger_df["area_tiger"] = tiger_df['geometry'].area
    res_identity = tiger_df.overlay(df_layer, how='union')
    res_identity["area"] = res_identity['geometry'].area
    res_identity["percent_overlay"] = res_identity["area"]/res_identity["area_tiger"]
    res_identity.to_csv(r'./out.csv')
    print(res_identity)



# function builds the api URL from tract_code, state_code, county_code, and attribute ids. 
def build_census_url(tract_code, state_code, county_code, attribute_ids):
    attributes = ','.join(attribute_ids)
    census_url = r'https://api.census.gov/data/2019/acs/acs5?get={}&in=state:{}&in=county:{}&for=tract:{}'\
                .format(attributes, state_code, county_code, tract_code)
    return census_url

# function makes a single api call and collects results in a pandas dataframe
def make_census_api_call(census_url):
    # make API call to Census
    resp = requests.get(census_url)
    if resp.status_code != 200:
        # this means something went wrong
        resp.raise_for_status()
       
    # retrieve data as json and convert to Pandas Dataframe
    data = resp.json()
    headers = data.pop(0)
    df = pd.DataFrame(data, columns=headers)

    # convert values that are not state, county, or tract to numeric type
    cols=[i for i in df.columns if i not in ["state","county","tract"]]
    for col in cols:
        df[col]=pd.to_numeric(df[col])

    return df

def make_tiger_api_call(bbox):
    bbox = ",".join([str(i) for i in bbox])
    tiger_url = r'https://tigerweb.geo.census.gov/arcgis/rest/services/Generalized_ACS2019/Tracts_Blocks/MapServer/3/query?where=&text=&objectIds=&time=&geometry={}&geometryType=esriGeometryEnvelope&inSR=4269&spatialRel=esriSpatialRelIntersects&distance=&units=esriSRUnit_Foot&relationParam=&outFields=GEOID,TRACT&returnGeometry=true&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=&havingClause=&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&historicMoment=&returnDistinctValues=false&resultOffset=&resultRecordCount=&returnExtentOnly=false&datumTransformation=&parameterValues=&rangeValues=&quantizationParameters=&featureEncoding=esriDefault&f=geojson'.format(bbox)
    df_tiger = geopandas.read_file(tiger_url)
    return df_tiger
if __name__ == '__main__':
    app.run()
