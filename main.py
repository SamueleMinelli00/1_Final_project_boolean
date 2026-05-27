###importing libraries
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import datetime as dt
import numpy as np
import seaborn as sns

###loading data
#paths
distances_to_WAP_centroid_path = r'C:\Users\183632\OneDrive\Culture\0-UNI\2025-26_Boolean\Data Analytics\6_Final project\1_Final_project_boolean\Data\acled_distances_to_WAP_centroid.geojson'
net_distances_to_WAP_path = r'C:\Users\183632\OneDrive\Culture\0-UNI\2025-26_Boolean\Data Analytics\6_Final project\1_Final_project_boolean\Data\acled_net_distances_updated.geojson'

###loading GDFs from the specified paths
distances_to_WAP_centroid = gpd.read_file(distances_to_WAP_centroid_path)
net_distances_to_WAP = gpd.read_file(net_distances_to_WAP_path)

#print(distances_to_WAP_centroid.head(5))
#distances_to_WAP_centroid.info()
#print(net_distances_to_WAP.head(5))
#net_distances_to_WAP.info()

###merging files
ACLED_to_WAP_merged = distances_to_WAP_centroid.merge(
    net_distances_to_WAP[['event_id_c', 'distance_to_perimeter']],
    how='left',
    on='event_id_c'
)
ACLED_to_WAP_merged.info()
pd.set_option('display.max_columns', None)
#print(ACLED_to_WAP_merged.head(5))

###Dropping unnecessary columns
ACLED_to_WAP_clean = ACLED_to_WAP_merged.drop(columns=['iso', 'source_sca', 'timestamp', 'event_id_1', 'submission', 'source_lin', 'misc', 'coder', 'temp_regio', 'upload_day', 'sub_sys_de', 'overseas_t', 'HubName', 'vertex_ind', 'vertex_pos', 'vertex_par', 'vertex_p_1', 'distance', 'angle', 'geometry'])
#print(ACLED_to_WAP_clean.info())

###rename columns for clarity
ACLED_to_WAP_clean.rename(columns={
   'HubDist': 'distance_to_centroid_km',
   'distance_to_perimeter': 'distance_to_perimeter_km',
   'sub_event_': 'SET',
   'event_id_c': 'event_id'
}, inplace=True)
#print(ACLED_to_WAP_clean.info())

###convert distances into km (float) with two decimal numbers
ACLED_to_WAP_clean['distance_to_centroid_km'] = (ACLED_to_WAP_clean['distance_to_centroid_km']/1000).round(2)
ACLED_to_WAP_clean['distance_to_perimeter_km'] = (ACLED_to_WAP_clean['distance_to_perimeter_km']/1000).round(2)
#print(ACLED_to_WAP_clean.head(5))

###Filter by A1 and A2 (JNIM)
ACLED_to_WAP_clean = ACLED_to_WAP_clean[
    (ACLED_to_WAP_clean['actor1'] == 'JNIM: Group for Support of Islam and Muslims') |
    (ACLED_to_WAP_clean['actor2'] == 'JNIM: Group for Support of Islam and Muslims')
    ]

# display(ACLED_to_WAP_clean['actor1'].unique())
# display(ACLED_to_WAP_clean['actor2'].unique())

#print(ACLED_to_WAP_clean.info())

###Dropping unnecessary Sub Event Types (SETs)
SET_to_drop = ['Other']
'''
I am dropping only other as I am rather interested in all the events involving JNIM whether violent or not.
The scope of the project is to measure the width of the operations of the group rather than its violent dynamics
'''
ACLED_to_WAP_clean = ACLED_to_WAP_clean[~ACLED_to_WAP_clean['SET'].isin(SET_to_drop)]

#print(ACLED_to_WAP_clean['SET'].unique())

###convert event_date to datetime
ACLED_to_WAP_clean['event_date'] = pd.to_datetime(ACLED_to_WAP_clean['event_date'])

###extract month and calculate trimester
# Extract month and calculate trimester
ACLED_to_WAP_clean['month'] = ACLED_to_WAP_clean['event_date'].dt.month
ACLED_to_WAP_clean['trimester'] = ((ACLED_to_WAP_clean['month'] - 1) // 3) + 1
ACLED_to_WAP_clean['year_trimester'] = ACLED_to_WAP_clean['event_date'].dt.strftime('%Y') + '-Q' + ACLED_to_WAP_clean['event_date'].dt.quarter.astype(str)

print("DataFrame with 'month', 'trimester', and 'year_trimester' columns:")
print(ACLED_to_WAP_clean[['event_date', 'month', 'trimester', 'year_trimester']].head())