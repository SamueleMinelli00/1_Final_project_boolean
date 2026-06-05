'''
Permutation Tests
Year; Semester; Trimester

HP
The avg distances (both centroid and perimeter) between JNIM activities and the WAP complex in the first period (2018-2021) are smaller than the avg distances (both centroid and perimeter) of the second studied period (2022-2025)

If not falsified, the results might statistically suggest that JNIM (Katiba Hanifa) has effectively exploited the WAP complex as an HUB to expand its activities to other areas (e.g. NE, BF, BJ, TG)

H0: treatment (second period) = control (first period)

H1: treatment > control
'''

##
###TRIMESTERS
##

#Importing useful gdf created in main.py
from main import year_trimester_gdf
#importing useful libraries
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import datetime as dt
import numpy as np
import seaborn as sns


year_trimester_gdf = year_trimester_gdf[year_trimester_gdf['year'] != 2026]
results_gdf = []
results_gdf = pd.DataFrame(results_gdf)

treatment_trimester = year_trimester_gdf[year_trimester_gdf['cluster_category'] != 0]
control_trimester = year_trimester_gdf[year_trimester_gdf['cluster_category'] == 0]

#print(control_trimester.head(16))

#Centroid_trimester
mu_control_trimester_centroid = np.mean(control_trimester['avg_dist_centroid_year_trimester'])
print(mu_control_trimester_centroid)
mu_treatment_trimester_centroid = np.mean(treatment_trimester['avg_dist_centroid_year_trimester'])
print(mu_treatment_trimester_centroid)
mu_diff_trimester_centroid = (mu_treatment_trimester_centroid - mu_control_trimester_centroid).round(2)
print(mu_diff_trimester_centroid)
print(f'mu_diff_trimester_centroid: {mu_diff_trimester_centroid}')




#Perimeter
mu_control_trimester_perimeter = np.mean(control_trimester['avg_dist_perimeter_year_trimester'])
print(mu_control_trimester_perimeter)
mu_treatment_trimester_perimeter = np.mean(treatment_trimester['avg_dist_perimeter_year_trimester'])
print(mu_treatment_trimester_perimeter)
mu_diff_trimester_perimeter = (mu_treatment_trimester_perimeter - mu_control_trimester_perimeter).round(2)
print(f'mu_diff_trimester_perimeter: {mu_diff_trimester_perimeter}')


##Performing permutations
combined_trimester_data = pd.concat([control_trimester, treatment_trimester], ignore_index=True)

n_permutations = 20000
mu_diff_samples_centroid = []
mu_diff_samples_perimeter = []


for i in range (n_permutations):
  sample1_indices = combined_trimester_data.sample(frac=0.5, replace=False).index
  sample2_indices = combined_trimester_data.index.difference(sample1_indices)

  sample1_data = combined_trimester_data.loc[sample1_indices]
  sample2_data = combined_trimester_data.loc[sample2_indices]

  #centroid
  mu_diff_temp_centroid = np.mean(sample1_data['avg_dist_centroid_year_trimester']) - np.mean(sample2_data['avg_dist_centroid_year_trimester'])
  mu_diff_samples_centroid.append(mu_diff_temp_centroid)

  #perimeter
  mu_diff_temp_perimeter = np.mean(sample1_data['avg_dist_perimeter_year_trimester']) - np.mean(sample2_data['avg_dist_perimeter_year_trimester'])
  mu_diff_samples_perimeter.append(mu_diff_temp_perimeter)

print(f'Completed {n_permutations} permutations')

##Plotting the results
#Centroid
sns.histplot(mu_diff_samples_centroid)
plt.axvline(mu_diff_trimester_centroid, 0, 1, color='r', linestyle='--')
plt.title('Distribution of Centroid Differences (Permutation Test)')
plt.show()
print('mu_diff', round(mu_diff_trimester_centroid, 2))

#Perimeter
sns.histplot(mu_diff_samples_perimeter)
plt.axvline(mu_diff_trimester_perimeter, 0, 1, color='r', linestyle='--')
plt.title('Distribution of Perimeter Differences (Permutation Test)')
plt.show()
print('mu_diff', round(mu_diff_trimester_perimeter, 2))

'''Setting the significance level to 5% and Calculating p-values'''

#Centroids
p_value_trimester_centroid = sum(mu_diff_samples_centroid>mu_diff_trimester_centroid)/n_permutations
print(f'p_value_trimester_centroid: {p_value_trimester_centroid}')
p_value_trimester_centroid_percent = (p_value_trimester_centroid*100).round(2)
print(f'p_value_trimester_centroid_percentile: {p_value_trimester_centroid_percent} %')

#Perimeter
p_value_trimester_perimeter = sum(mu_diff_samples_perimeter>mu_diff_trimester_perimeter)/n_permutations
print(f'p_value_trimester_perimeter: {p_value_trimester_perimeter}')
p_value_trimester_perimeter_percent = (p_value_trimester_perimeter*100).round(2)
print(f'p_value_trimester_perimeter_percent: {p_value_trimester_perimeter_percent} %')

#Appending results to the results_gdf
results_gdf = pd.concat([results_gdf, pd.DataFrame([{
  'mu_diff_trimester_centroid': mu_diff_trimester_centroid,
  'mu_diff_trimester_perimeter': mu_diff_trimester_perimeter,
  'p_value_trimester_centroid': p_value_trimester_centroid,
  'p_value_trimester_centroid_percent': p_value_trimester_centroid_percent,
  'p_value_trimester_perimeter': p_value_trimester_perimeter,
  'p_value_trimester_perimeter_percent': p_value_trimester_perimeter_percent
}])], ignore_index=True)

'''
p-value < alpha: 
the difference between treatment (second period) and control (first period) is statistically significant, H0 is refuted.
'''