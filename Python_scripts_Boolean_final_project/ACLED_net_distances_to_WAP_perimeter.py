import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon, Point, MultiPolygon # Added MultiPolygon
from shapely.ops import unary_union
from shapely import wkt # Import shapely.wkt
from qgis.core import QgsProject, QgsVectorLayer, QgsRasterLayer, QgsCoordinateReferenceSystem
from geopandas import GeoSeries # Explicitly import GeoSeries for robust geometry handling
import processing

# --- Helper function to convert QgsVectorLayer to GeoDataFrame ---
def qgis_vector_layer_to_gdf(qgis_layer):
    features_list = [] # List to store dictionaries of attributes + geometry
    field_names = [field.name() for field in qgis_layer.fields()]

    for feature in qgis_layer.getFeatures():
        row_data = {}
        # Extract attributes
        for i, attr_value in enumerate(feature.attributes()):
            row_data[field_names[i]] = attr_value

        # Extract geometry
        geom = feature.geometry()
        shapely_geom = None
        if geom and geom.isGeosValid():
            shapely_geom_wkt = geom.asWkt()
            try:
                shapely_geom = wkt.loads(shapely_geom_wkt)
            except Exception as e:
                print(f"Warning: Could not load WKT for feature {feature.id()} in layer '{qgis_layer.name()}'. Error: {e}")
                print(f"Problematic WKT (first 100 chars): {shapely_geom_wkt[:100]}...")
        else:
            print(f"Warning: Invalid or empty geometry found for feature {feature.id()} in layer {qgis_layer.name()}. Geometry will be None.")

        row_data['geometry'] = shapely_geom # Add geometry to the dictionary
        features_list.append(row_data)

    crs_wkt = "EPSG:4326"
    qgis_crs = qgis_layer.crs()
    if qgis_crs.isValid():
        crs_wkt = qgis_crs.toWkt()
    else:
        print(f"Warning: QGIS layer '{qgis_layer.name()}' has an invalid or undefined CRS. Using default: {crs_wkt}.")

    # Create GeoDataFrame
    if not features_list:
        # Create an empty GeoDataFrame with geometry column and other attribute columns
        all_columns = field_names + ['geometry']
        gdf = gpd.GeoDataFrame(columns=all_columns, geometry=[], crs=crs_wkt)
    else:
        gdf = gpd.GeoDataFrame(features_list, crs=crs_wkt)
    
    print(f"DEBUG: GeoDataFrame from '{qgis_layer.name()}' columns: {gdf.columns.tolist()}")
    print(f"DEBUG: GeoDataFrame from '{qgis_layer.name()}' head:")
    print(gdf.head())

    return gdf


# --- Step 1: Get the QGIS active layers ---
WAP_name = 'WAP_complex_no_holes'
ACLED_name = 'ACLED_WAP_complex'

# Get WAP_layer
layers = QgsProject.instance().mapLayersByName(WAP_name)
if layers:
    qgis_WAP_layer = layers[0]
    print(f"Successfully retrieved layer '{qgis_WAP_layer.name()}'")
else:
    raise ValueError(f"Layer '{WAP_name}' not found in QGIS project.")

# Get ACLED_layer
layers = QgsProject.instance().mapLayersByName(ACLED_name)
if layers:
    qgis_ACLED_layer = layers[0]
    print(f"Successfully retrieved layer '{qgis_ACLED_layer.name()}'")
else:
    raise ValueError(f"Layer '{ACLED_name}' not found in QGIS project.")


# --- Step 2: Convert QGIS layers to GeoDataFrames ---
WAP_boundary_gdf = qgis_vector_layer_to_gdf(qgis_WAP_layer)
ACLED_points_gdf = qgis_vector_layer_to_gdf(qgis_ACLED_layer)

print("WAP_boundary_gdf head:")
print(WAP_boundary_gdf.head())
print("ACLED_points_gdf head:")
print(ACLED_points_gdf.head())


# --- Step 3: Ensure consistent projections ---
# Reproject to a suitable projected CRS (e.g., UTM Zone 30N, EPSG:32630) for accurate distance calculation
target_crs = "EPSG:32630" # UTM Zone 30N (common for West Africa)

WAP_boundary_gdf_proj = WAP_boundary_gdf
if WAP_boundary_gdf.crs != target_crs:
    WAP_boundary_gdf_proj = WAP_boundary_gdf.to_crs(target_crs)

ACLED_points_gdf_proj = ACLED_points_gdf
if ACLED_points_gdf.crs != target_crs:
    ACLED_points_gdf_proj = ACLED_points_gdf.to_crs(target_crs)


# --- Step 4: Calculate the perimeter and aggregated polygon ---
# Check if WAP_boundary_gdf_proj is empty before attempting unary_union
if WAP_boundary_gdf_proj.empty:
    raise ValueError("WAP_boundary_gdf_proj is empty, cannot calculate perimeter.")

# Ensure that the geometry column contains Shapely objects
if not WAP_boundary_gdf_proj.geometry.apply(lambda x: isinstance(x, (Polygon, Point, MultiPolygon))).all():
    raise TypeError("WAP_boundary_gdf_proj geometry column does not contain valid Shapely objects.")

park_polygon = unary_union(WAP_boundary_gdf_proj.geometry)
WAP_perimeter = park_polygon.boundary

# --- Step 5: Define the net distance function ---
def calculate_net_distance(point_geometry, boundary_polygon, perimeter_geometry):
    distance = point_geometry.distance(perimeter_geometry)
    if boundary_polygon.contains(point_geometry):
        return -distance
    else:
        return distance

# --- Step 6: Calculate distance for each point ---
if ACLED_points_gdf_proj.empty:
    print("ACLED_points_gdf_proj is empty, no distances to calculate.")
    ACLED_points_gdf_proj['distance_to_perimeter'] = [] # Add an empty column for consistency
else:
    # Ensure that the geometry column contains Shapely objects
    if not ACLED_points_gdf_proj.geometry.apply(lambda x: isinstance(x, (Point))).all():
        raise TypeError("ACLED_points_gdf_proj geometry column does not contain valid Shapely Point objects.")

    else:
        ACLED_points_gdf_proj['distance_to_perimeter'] = ACLED_points_gdf_proj.geometry.apply(
        lambda geom: calculate_net_distance(geom, park_polygon, WAP_perimeter))

        # Check if 'event_id_cnty' exists in ACLED_points_gdf before attempting to assign
        if 'event_id_c' in ACLED_points_gdf.columns:
            ACLED_points_gdf_proj['event_id_c'] = ACLED_points_gdf ['event_id_c']
            pd.set_option('display.max_columns', None) #no max number of columns
        else:
            print("Warning: 'event_id_cnty' column not found in ACLED_points_gdf (from QGIS layer). ")
            print("Please ensure your 'ACLED_WAP_complex' QGIS layer contains this attribute, ")
            print("or consider explicitly merging attributes from your 'acled_df' (from Excel) ")
            print("if you intend to use those IDs.")

print("\nACLED Points GeoDataFrame with 'distance_to_perimeter' column:")
print(ACLED_points_gdf_proj.head(1))


###Exporting ACLED_points_gdf_proj as geojson###


# Define a local output path (e.g., in the /tmp/ directory of the Colab environment)
output_dir = r'C:\Users\183632\Desktop\GEO\2_Python_scripts_QGIS\Geojson'

# Ensure the directory exists
if not os.path.exists(output_dir):
    print('the dir does not exist')

# Define the full local path for the GeoJSON file
acled_net_distances_updated = os.path.join(output_dir, 'acled_net_distances_updated.geojson')

# Save the ACLED points GeoDataFrame to the local GeoJSON file
ACLED_points_gdf_proj.to_file(acled_net_distances_updated, driver='GeoJSON')

print(f"ACLED points GeoDataFrame saved locally to: {acled_net_distances_updated}")