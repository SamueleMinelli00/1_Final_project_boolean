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
### SEMESTERS
##


#Importing useful gdf created in main.py
from main import year_semester_gdf
#importing useful libraries
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import datetime as dt
import numpy as np
import seaborn as sns

year_semester_gdf = year_semester_gdf[year_semester_gdf['year'] != 2026]

control_semester = year_semester_gdf[year_semester_gdf['cluster_category'] == 0]
treatment_semester = year_semester_gdf[year_semester_gdf['cluster_category'] != 0]

# print('Control Semester Data:')
# print(control_semester.head())
# print('\nTreatment Semester Data:')
# print(treatment_semester.head())

#Centroid_semester
mu_control_semester_centroid = np.mean(control_semester['avg_dist_centroid_year_semester'])
mu_treatment_semester_centroid = np.mean(treatment_semester['avg_dist_centroid_year_semester'])
mu_diff_semester_centroid = (mu_treatment_semester_centroid - mu_control_semester_centroid).round(2)
print(f'mu_diff_semester_centroid: {mu_diff_semester_centroid}')

#Perimeter_semester
mu_control_semester_perimeter = np.mean(control_semester['avg_dist_perimeter_year_semester'])
mu_treatment_semester_perimeter = np.mean(treatment_semester['avg_dist_perimeter_year_semester'])
mu_diff_semester_perimeter = (mu_treatment_semester_perimeter - mu_control_semester_perimeter).round(2)
print(f'mu_diff_semester_perimeter: {mu_diff_semester_perimeter}')

##performing permutations
combined_semester_data = pd.concat([control_semester, treatment_semester], ignore_index=True)

n_permutations = 20000
mu_diff_samples_centroid_semester = []
mu_diff_samples_perimeter_semester = []


for i in range (n_permutations):
  sample1_indices_semester = combined_semester_data.sample(frac=0.5, replace=False).index
  sample2_indices_semester = combined_semester_data.index.difference(sample1_indices_semester)

  sample1_data_semester = combined_semester_data.loc[sample1_indices_semester]
  sample2_data_semester = combined_semester_data.loc[sample2_indices_semester]

  #centroid
  mu_diff_temp_centroid_semester = np.mean(sample1_data_semester['avg_dist_centroid_year_semester']) - np.mean(sample2_data_semester['avg_dist_centroid_year_semester'])
  mu_diff_samples_centroid_semester.append(mu_diff_temp_centroid_semester)

  #perimeter
  mu_diff_temp_perimeter_semester = np.mean(sample1_data_semester['avg_dist_perimeter_year_semester']) - np.mean(sample2_data_semester['avg_dist_perimeter_year_semester'])
  mu_diff_samples_perimeter_semester.append(mu_diff_temp_perimeter_semester)

print(f'Completed {n_permutations} permutations for semester data')

##Plotting the results
#Centroid_semester
sns.histplot(mu_diff_samples_centroid_semester)
plt.axvline(mu_diff_semester_centroid, 0, 1, color='r', linestyle='--')
plt.title('Distribution of Centroid Differences (Permutation Test - Semester)')
plt.show()
print('mu_diff_semester_centroid', round(mu_diff_semester_centroid, 2))

#Perimeter_semester
sns.histplot(mu_diff_samples_perimeter_semester)
plt.axvline(mu_diff_semester_perimeter, 0, 1, color='r', linestyle='--')
plt.title('Distribution of Perimeter Differences (Permutation Test - Semester)')
plt.show()
print('mu_diff_semester_perimeter', round(mu_diff_semester_perimeter, 2))

''' Setting the significance level to 5% '''
#Calculating the p-value semester centroid

p_value_semester_centroid = sum(mu_diff_samples_centroid_semester > mu_diff_semester_centroid) / n_permutations
print(f'p_value_semester_centroid: {p_value_semester_centroid}')
p_value_semester_centroid_percent = (p_value_semester_centroid * 100).round(2)
print(f'p_value_semester_centroid_percentile: {p_value_semester_centroid_percent} %')

#Calculating the p-value semester perimeter

p_value_semester_perimeter = sum(mu_diff_samples_perimeter_semester > mu_diff_semester_perimeter) / n_permutations
print(f'p_value_semester_perimeter: {p_value_semester_perimeter}')
p_value_semester_perimeter_percent = (p_value_semester_perimeter * 100).round(2)
print(f'p_value_semester_perimeter_percent: {p_value_semester_perimeter_percent} %')

'''
the p-value < alpha: 
the difference between treatment (second period) and control (first period) is statistically significant, H0 is refuted.
'''