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
###YEAR
##

#Importing useful gdf created in main.py
from main import single_years_gdf
from permutations_trimesters import results_gdf
#importing useful libraries
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import datetime as dt
import numpy as np
import seaborn as sns


single_years_gdf = single_years_gdf[single_years_gdf['year'] != 2026] #removing 2026 as it is not a full year and would bias the results and it would create two clusters with different dimensions


control_year = single_years_gdf[single_years_gdf['cluster_category'] == 0]
treatment_year = single_years_gdf[single_years_gdf['cluster_category'] != 0]


#Centroid_year
mu_control_year_centroid = np.mean(control_year['avg_dist_centroid_year'])
mu_treatment_year_centroid = np.mean(treatment_year['avg_dist_centroid_year'])
mu_diff_year_centroid = (mu_treatment_year_centroid - mu_control_year_centroid).round(2)
print(f'mu_diff_year_centroid: {mu_diff_year_centroid}')

#Perimeter_year
mu_control_year_perimeter = np.mean(control_year['avg_dist_perimeter_year'])
mu_treatment_year_perimeter = np.mean(treatment_year['avg_dist_perimeter_year'])
mu_diff_year_perimeter = (mu_treatment_year_perimeter - mu_control_year_perimeter).round(2)
print(f'mu_diff_year_perimeter: {mu_diff_year_perimeter}')

##performing permutations
combined_year_data = pd.concat([control_year, treatment_year], ignore_index=True)

n_permutations = 20000
mu_diff_samples_centroid_year = []
mu_diff_samples_perimeter_year = []

for i in range (n_permutations):
  sample1_indices_year = combined_year_data.sample(frac=0.5, replace=False).index
  sample2_indices_year = combined_year_data.index.difference(sample1_indices_year)

  sample1_data_year = combined_year_data.loc[sample1_indices_year]
  sample2_data_year = combined_year_data.loc[sample2_indices_year]

  #centroid
  mu_diff_temp_centroid_year = np.mean(sample1_data_year['avg_dist_centroid_year']) - np.mean(sample2_data_year['avg_dist_centroid_year'])
  mu_diff_samples_centroid_year.append(mu_diff_temp_centroid_year)

  #perimeter
  mu_diff_temp_perimeter_year = np.mean(sample1_data_year['avg_dist_perimeter_year']) - np.mean(sample2_data_year['avg_dist_perimeter_year'])
  mu_diff_samples_perimeter_year.append(mu_diff_temp_perimeter_year)

print(f'Completed {n_permutations} permutations for year data')

##Plotting the results
#Centroid_year
sns.histplot(mu_diff_samples_centroid_year)
plt.axvline(mu_diff_year_centroid, 0, 1, color='r', linestyle='--')
plt.title('Distribution of Centroid Differences (Permutation Test - Year)')
plt.show()
print('mu_diff_year_centroid', round(mu_diff_year_centroid, 2))

#Perimeter_year
sns.histplot(mu_diff_samples_perimeter_year)
plt.axvline(mu_diff_year_perimeter, 0, 1, color='r', linestyle='--')
plt.title('Distribution of Perimeter Differences (Permutation Test - Year)')
plt.show()
print('mu_diff_year_perimeter', round(mu_diff_year_perimeter, 2))


''' Setting the significance level to 5% '''
#Calculating the p-value year centroid

p_value_year_centroid = sum(mu_diff_samples_centroid_year > mu_diff_year_centroid) / n_permutations
print(f'p_value_year_centroid: {p_value_year_centroid}')
p_value_year_centroid_percent = (p_value_year_centroid * 100).round(2)
print(f'p_value_year_centroid_percentile: {p_value_year_centroid_percent} %')

#Calculating the p-value year perimeter

p_value_year_perimeter = sum(mu_diff_samples_perimeter_year > mu_diff_year_perimeter) / n_permutations
print(f'p_value_year_perimeter: {p_value_year_perimeter}')
p_value_year_perimeter_percent = (p_value_year_perimeter * 100).round(2)
print(f'p_value_year_perimeter_percent: {p_value_year_perimeter_percent} %')

#appending results to the results_gdf
results_gdf.append({
  'mu_diff_year_centroid': mu_diff_year_centroid,
  'mu_diff_year_perimeter': mu_diff_year_perimeter,
  'p_value_year_centroid': p_value_year_centroid,
  'p_value_year_centroid_percent': p_value_year_centroid_percent,
  'p_value_year_perimeter': p_value_year_perimeter,
  'p_value_year_perimeter_percent': p_value_year_perimeter_percent
})

'''
the p-value < alpha only for the centroid distances: the difference between treatment (second period) and control (first period) is statistically significant, H0 is refuted.
H0 is accepted for the perimter distances: the difference between treatment (second period) and control (first period) is not statistically significant,
'''