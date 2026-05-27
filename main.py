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
distances_to_WAP_centroid.info()
#print(net_distances_to_WAP.head(5))
net_distances_to_WAP.info()

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
print(ACLED_to_WAP_clean.info())

