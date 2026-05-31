import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon, Point
from shapely.ops import unary_union

# --- Ensured projections are consistent and correct variable assignment ---
WAP_boundary = WAP_complex_no_holes.to_crs(epsg=32630)
points_proj = ACLED_WAP_complex.to_crs(epsg=32630) # Correctly assign to points_proj

# Get the aggregated boundary geometry (union of all polygons in WAP_boundary)
park_polygon = unary_union(WAP_boundary.geometry)
# Get the perimeter geometry of the WAP complex from the aggregated polygon
WAP_perimeter = park_polygon.boundary

# Defining a function to calculate net distance
def calculate_net_distance(point_geometry, boundary_polygon, perimeter_geometry):
    """
    Calculates the signed distance of a single point to a boundary perimeter.
    Distance is negative if the point is inside the boundary, positive if outside.

    Args:
        point_geometry (shapely.geometry.Point): The geometry of a single point.
        boundary_polygon (shapely.geometry.Polygon or MultiPolygon): The geometry of the boundary area (e.g., WAP complex).
        perimeter_geometry (shapely.geometry.LineString or MultiLineString): The geometry of the boundary perimeter.

    Returns:
        float: The signed distance.
    """
    distance = point_geometry.distance(perimeter_geometry)

    # Check if the point is inside the boundary polygon
    if boundary_polygon.contains(point_geometry):
        return -distance
    else:
        return distance


# Calculate distance for each point
points_proj['distance_to_perimeter'] = points_proj.geometry.apply(
    lambda geom: calculate_net_distance(geom, park_polygon, WAP_perimeter)
) # Corrected function name and added closing parenthesis

print("\nPoints GeoDataFrame with 'distance_to_perimeter' column:")
display(points_proj.head(10))
