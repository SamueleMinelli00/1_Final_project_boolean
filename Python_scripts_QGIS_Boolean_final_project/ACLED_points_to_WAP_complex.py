from shapely.geometry import LineString

# Ensure ACLED_points_gdf_proj and WAP_perimeter are already defined and in a projected CRS

if ACLED_points_gdf_proj.empty or WAP_perimeter.is_empty:
    print("Cannot create connection lines: ACLED points or WAP perimeter is empty.")
    shortest_path_lines_gdf = gpd.GeoDataFrame(geometry=[], crs=ACLED_points_gdf_proj.crs)
else:
    # List to store LineString geometries
    shortest_paths = []

    # Iterate through each point in the ACLED GeoDataFrame
    for idx, row in ACLED_points_gdf_proj.iterrows():
        point = row.geometry
        
        # Find the closest point on the WAP_perimeter to the current ACLED point
        # The `project` method returns the distance along the perimeter to the closest point
        closest_point_on_perimeter = WAP_perimeter.interpolate(WAP_perimeter.project(point))
        
        # Create a LineString from the ACLED point to the closest point on the perimeter
        shortest_paths.append(LineString([point, closest_point_on_perimeter]))

    # Create a new GeoDataFrame from these LineStrings
    shortest_path_lines_gdf = gpd.GeoDataFrame(geometry=shortest_paths, crs=ACLED_points_gdf_proj.crs)

print("Shortest path lines GeoDataFrame head:")
print(shortest_path_lines_gdf.head())
print(f"Total {len(shortest_path_lines_gdf)} shortest path lines created.")