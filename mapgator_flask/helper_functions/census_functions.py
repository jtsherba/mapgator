from collections import defaultdict
import numpy as np
import pandas as pd

# define other helper functions
def calc_sum(df, attribute_id):
    return str(df[attribute_id].sum())

def calc_normalized(df, attribute_id, attribute_id2):
    if df[attribute_id2].sum() == 0:
        return 0
    else:
        return (df[attribute_id].sum()/df[attribute_id2].sum())
    
def calc_normalized_100(df, attribute_id, attribute_id2):
    if df[attribute_id2].sum() == 0:
        return 0
    else:
        return (1-(df[attribute_id].sum()/df[attribute_id2].sum()))

def calc_sum_normalized(df, attribute_list, attribute_id2):
    if df[attribute_id2].sum()==0:
        return 0
    else:
        sum_of_attributes = 0
        for attribute_id in attribute_list:
            sum_of_attributes+=df[attribute_id].sum()
        return sum_of_attributes/df[attribute_id2].sum()

# function runs all calcs for each neighborhood or supervisor district
def calc_socio_economic_data(df, block_group_lookup):
   
    # create empty dictionary to add calculated attribute information to
    all_calc_data = defaultdict(dict) 
    # calculate all stats for each neighborhood
    for nb_name, block_group_ids in block_group_lookup.items():
        # extract attribute information for tracks associated with a neighborhood
        if nb_name =="sf":
            tract_df = df
        else:
            tract_df = df[df['tract'].isin(block_group_ids.keys())]
   
            all_columns =  list(tract_df.columns)
            for column in ['state', 'county', 'tract']:
                all_columns.remove(column)
            for col_id, percent in block_group_lookup[nb_name].items():
                for column in all_columns:
                   
                    tract_df[column] = np.where(tract_df['tract']==col_id, tract_df[column]*(float(percent)/100), tract_df[column])
      
 
         
        # build dictionary with all stats for a neighborhood
        all_calc_data_nb = all_calc_data[str(nb_name)]
        # population
        all_calc_data_nb["Percent Female"] = calc_normalized(tract_df, 'B01001_026E', 'B01001_001E')
        # race and ethnicity stats
        all_calc_data_nb["Asian"] = calc_normalized(tract_df, 'B02001_005E', 'B02001_001E')
        all_calc_data_nb["Black/African American"] = calc_normalized(tract_df, 'B02001_003E', 'B02001_001E')
        all_calc_data_nb["White"] = calc_normalized(tract_df, 'B02001_002E', 'B02001_001E')
        all_calc_data_nb["Native American Indian"] = calc_normalized(tract_df, 'B02001_005E', 'B02001_001E')
        all_calc_data_nb["Native Hawaiian/Pacific Islander"] = calc_normalized(tract_df, 'B02001_006E', 'B02001_001E')
        all_calc_data_nb["Other/Two or More Races"] = calc_sum_normalized(tract_df, ['B02001_008E', 'B02001_007E'], 'B02001_001E')
        all_calc_data_nb["% Latino (of Any Race)"] = calc_normalized(tract_df, 'B03001_003E', 'B03001_001E')
        all_calc_data_nb["Total People of Color"] = calc_normalized_100(tract_df, 'B02001_002E', 'B02001_001E')
        # disability
        all_calc_data_nb["% of people with disabilities"] = calc_sum_normalized(tract_df, ['C18108_003E', 'C18108_004E', 'C18108_007E', 'C18108_008E', 'C18108_011E', 'C18108_012E'], 'C18108_001E')
        # age
        all_calc_data_nb["0-4 Years"] = calc_sum_normalized(tract_df, ['B01001_003E', 'B01001_027E'], 'B01001_001E')
        all_calc_data_nb["5-17 Years"] = calc_sum_normalized(tract_df, ['B01001_004E', 'B01001_005E', 'B01001_006E', 'B01001_028E', 'B01001_029E', 'B01001_030E'],'B01001_001E')
        all_calc_data_nb["60 and Older"] = calc_sum_normalized(tract_df, ['B01001_018E', 'B01001_019E', 'B01001_020E', 'B01001_021E', 'B01001_022E', 'B01001_023E', 'B01001_024E', 'B01001_025E', 'B01001_042E', 'B01001_043E', 'B01001_044E', 'B01001_045E', 'B01001_046E', 'B01001_047E', 'B01001_048E', 'B01001_049E'], 'B01001_001E')
        # nativity
        all_calc_data_nb["Foreign Born"] = calc_normalized(tract_df, 'B05002_013E', 'B05002_001E')
        # education
        all_calc_data_nb["% of individuals over 25 with at least a high school degree"] = calc_sum_normalized(tract_df, ['B15003_017E', 'B15003_018E', 'B15003_019E', 'B15003_020E', 'B15003_021E', 'B15003_022E', 'B15003_023E', 'B15003_024E', 'B15003_025E'], 'B15003_001E')
        # vehicles
        all_calc_data_nb["Households with no Vehicle"] = calc_sum_normalized(tract_df, ['B25044_003E', 'B25044_010E'], 'B25044_001E')
        # housing 
        all_calc_data_nb["Renter Occupied"] = calc_normalized(tract_df, 'B25007_012E', 'B25007_001E')
        # linguistic isolation
        all_calc_data_nb["% of All Households"] = calc_sum_normalized(tract_df, ['B16003_002E', 'B16003_008E'], 'B16004_001E')
        all_calc_data_nb["% of Spanish-Speaking Households"] = calc_sum_normalized(tract_df, ['B16003_004E', 'B16003_009E'], 'B16004_001E')
        all_calc_data_nb["% of Asian-Speaking Households"] = calc_sum_normalized(tract_df, ['B16003_006E', 'B16003_011E'], 'B16004_001E')
        all_calc_data_nb["% of Other European-Speaking Households"] = calc_sum_normalized(tract_df, ['B16003_005E', 'B16003_010E'], 'B16004_001E')
        all_calc_data_nb["% of Households Speaking Other Languages"] = calc_sum_normalized(tract_df, ['B16003_007E', 'B16003_012E'], 'B16004_001E')
        #income
        all_calc_data_nb["Percent in Poverty"] = calc_normalized(tract_df, 'B17001_002E', 'B17001_001E')
    #return calc dictionary
    return all_calc_data

def calc_basic_census_data(df, block_group_lookup, census_variable):
    # create empty dictionary to add calculated attribute information to
    print(block_group_lookup)
    all_calc_data = defaultdict(dict) 
    # calculate all stats for each neighborhood
    for nb_name, block_group_ids in block_group_lookup.items():
        # extract attribute information for tracks associated with a neighborhood

        if nb_name =="sf":
            tract_df = df
        else:
            tract_df = df[df['tract'].isin(block_group_ids.keys())]
   
            all_columns =  list(tract_df.columns)
            for column in ['state', 'county', 'tract']:
                all_columns.remove(column)
            for col_id, percent in block_group_lookup[nb_name].items():
                for column in all_columns:
                   
                    tract_df[column] = np.where(tract_df['tract']==col_id, tract_df[column]*(float(percent)), tract_df[column])
      
 
        # build dictionary with all stats for a neighborhood
        all_calc_data_nb = all_calc_data[str(nb_name)]
        # population
     
        all_calc_data_nb["sample_data"] = calc_sum(tract_df, census_variable)

    return all_calc_data