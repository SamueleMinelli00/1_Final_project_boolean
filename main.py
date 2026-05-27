###importing libraries
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import contextily as ctx
import datetime as dt
import numpy as np
import seaborn as sns

###loading data
#paths
distances_to_WAP_centroid_path = r'C:\Users\183632\OneDrive\Culture\0-UNI\2025-26_Boolean\Data Analytics\6_Final project\1_Final_project_boolean\Data\acled_distances_to_WAP_centroid.geojson'
net_distances_to_WAP_path = r'C:\Users\183632\OneDrive\Culture\0-UNI\2025-26_Boolean\Data Analytics\6_Final project\1_Final_project_boolean\Data\acled_net_distances_updated.geojson'

#loading GDFs from the specified paths
distances_to_WAP_centroid = gpd.read_file(distances_to_WAP_centroid_path)
net_distances_to_WAP = gpd.read_file(net_distances_to_WAP_path)

print(distances_to_WAP_centroid.head(5))
distances_to_WAP_centroid.info()
print(net_distances_to_WAP.head(5))
net_distances_to_WAP.info()