### Define output paths for your GeoJSON files
output_dir = r'C:\Users\183632\Desktop\GEO\2_Python_scripts_QGIS\Try' # Adjust

### Ensure the output directory exists
import os
if not os.path.exists(output_dir):
    print('the dir does not exists')
'''
### Save shortest path lines
shortest_path_lines_output = os.path.join(output_dir, 'shortest_path_lines.geojson')
shortest_path_lines_gdf.to_file(shortest_path_lines_output, driver='GeoJSON')
print(f"Shortest path lines saved to: {shortest_path_lines_output}")

### Save WAP boundary
wap_boundary_output = os.path.join(output_dir, 'wap_boundary.geojson')
WAP_boundary_gdf_proj.to_file(wap_boundary_output, driver='GeoJSON')
print(f"WAP boundary saved to: {wap_boundary_output}")

### Save ACLED points
acled_points_output = os.path.join(output_dir, 'acled_points.geojson')
ACLED_points_gdf_proj.to_file(acled_points_output, driver='GeoJSON')
print(f"ACLED points saved to: {acled_points_output}")
'''

### ACLED_net_distances_updated
ACLED_net_distances_updated = os.path.join(output_dir, 'ACLED_net_distances_updated.geojson')
ACLED_net_distances_updated.to_file(ACLED_net_distances_updated, driver='GeoJSON')
print(f"ACLED points saved to: {ACLED_net_distances_updated}")

### ACLED_distances_to_WAP_centroid
ACLED_distances_to_WAP_centroid = os.path.join(output_dir, 'ACLED_distances_to_WAP_centroid.geojson')
ACLED_distances_to_WAP_centroid.to_file(ACLED_distances_to_WAP_centroid, driver='GeoJSON')
print(f"ACLED points saved to: {ACLED_distances_to_WAP_centroid}")

print("\nNow you can open these .geojson files as layers in QGIS.")