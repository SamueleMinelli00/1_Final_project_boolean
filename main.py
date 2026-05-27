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
   'event_id_c': 'event_id',
   'fataliti_1': 'fat_precision'
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

###extract month and calculate TRIMESTER
# Extract month and calculate trimester
ACLED_to_WAP_clean['month'] = ACLED_to_WAP_clean['event_date'].dt.month
ACLED_to_WAP_clean['trimester'] = ((ACLED_to_WAP_clean['month'] - 1) // 3) + 1
# Combine trimester and year
ACLED_to_WAP_clean['year_trimester'] = ACLED_to_WAP_clean['event_date'].dt.strftime('%Y') + '-Q' + ACLED_to_WAP_clean['event_date'].dt.quarter.astype(str)

#print(ACLED_to_WAP_clean.head())
#print(ACLED_to_WAP_clean.info())

###calculate SEMESTER
ACLED_to_WAP_clean['semester'] = ((ACLED_to_WAP_clean['month']-1)//6) +1
# Combine semester and year
ACLED_to_WAP_clean['year_semester'] = ACLED_to_WAP_clean['event_date'].dt.strftime('%Y') + '-S' + ACLED_to_WAP_clean['semester'].astype(str)
#print(ACLED_to_WAP_clean.head(5))

###Move columns
# Get the current list of columns
current_columns = ACLED_to_WAP_clean.columns.tolist()

# Define the new order for the temporal columns
# Remove them from their current position and insert them after 'event_date'
columns_to_move = ['month', 'trimester', 'year_trimester', 'semester', 'year_semester']

for col in columns_to_move:
    if col in current_columns:
        current_columns.remove(col)

# Find the index of 'event_date'
event_date_index = current_columns.index('event_date')

# Insert the temporal columns after 'event_date'
new_columns_order = current_columns[:event_date_index + 1] + columns_to_move + current_columns[event_date_index + 1:]

# Reindex the DataFrame with the new column order
ACLED_to_WAP_clean = ACLED_to_WAP_clean[new_columns_order]

print(ACLED_to_WAP_clean[ACLED_to_WAP_clean['trimester'] == 3].head(10))

##
###Calculate the mean distance to the centroid and perimeter for each trimester, semester and year
##

trimesters = ACLED_to_WAP_clean['year_trimester'].unique()
semesters = ACLED_to_WAP_clean['year_semester'].unique()
print(semesters)

##SEMESTERS
semester_data = []
for s in semesters:
  current_year = int(s.split('-')[0]) # Extract the year for the current semester
  avg_dist_centroid_year_semester = ACLED_to_WAP_clean[ACLED_to_WAP_clean['year_semester'] == s]['distance_to_centroid_km'].mean().round(2)
  avg_dist_perimeter_year_semester = ACLED_to_WAP_clean[ACLED_to_WAP_clean['year_semester'] == s]['distance_to_perimeter_km'].mean().round(2)

  # Determine cluster_category based on the current_year
  if current_year > 2021:
    cluster_cat = 1
  else:
    cluster_cat = 0

  semester_data.append({
   'year': current_year,
   'semester': s,
   'avg_dist_centroid_year_semester': avg_dist_centroid_year_semester,
   'avg_dist_perimeter_year_semester': avg_dist_perimeter_year_semester,
   'cluster_category': cluster_cat # Add cluster_category to the dictionary
  })

year_semester_gdf = gpd.GeoDataFrame(semester_data)
year_semester_gdf.sort_values(by='semester', inplace=True)
year_semester_gdf = year_semester_gdf.reset_index(drop=True)
#print(year_semester_gdf.head(33))

##TRIMESTERS
trimester_data = []
for t in trimesters:
  current_year = int(t.split('-')[0]) # Extract the year for the current trimester
  avg_dist_centroid_year_trimester = ACLED_to_WAP_clean[ACLED_to_WAP_clean['year_trimester'] == t]['distance_to_centroid_km'].mean().round(2)
  avg_dist_perimeter_year_trimester = ACLED_to_WAP_clean[ACLED_to_WAP_clean['year_trimester'] == t]['distance_to_perimeter_km'].mean().round(2)

  # Determine cluster_category based on the current_year
  if current_year > 2021:
    cluster_cat = 1
  else:
    cluster_cat = 0

  trimester_data.append({
   'year': current_year,
   'trimester': t,
   'avg_dist_centroid_year_trimester': avg_dist_centroid_year_trimester,
   'avg_dist_perimeter_year_trimester': avg_dist_perimeter_year_trimester,
   'cluster_category': cluster_cat
  })

year_trimester_gdf = gpd.GeoDataFrame(trimester_data)
year_trimester_gdf.sort_values(by='trimester', inplace=True)
year_trimester_gdf = year_trimester_gdf.reset_index(drop=True)
#print(year_trimester_gdf.head(33))

##YEAR
years = [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026]

yearly_data = []
for y in years:
  avg_dist_centroid_year = ACLED_to_WAP_clean[ACLED_to_WAP_clean['year'] == y]['distance_to_centroid_km'].mean().round(2)
  avg_dist_perimeter_year = ACLED_to_WAP_clean[ACLED_to_WAP_clean['year'] == y]['distance_to_perimeter_km'].mean().round(2)
  # Determine cluster_category based on the y
  if y > 2021:
    cluster_cat = 1
  else:
    cluster_cat = 0
  
  yearly_data.append({
      'year': y,
      'avg_dist_centroid_year': avg_dist_centroid_year,
      'avg_dist_perimeter_year': avg_dist_perimeter_year,
      'cluster_category': cluster_cat
  })


single_years_gdf = gpd.GeoDataFrame(yearly_data)
print("\nSingle Years GeoDataFrame:")
print(single_years_gdf.head(9))

