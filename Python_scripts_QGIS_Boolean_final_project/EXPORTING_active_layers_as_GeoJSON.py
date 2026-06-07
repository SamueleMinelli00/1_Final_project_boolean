from qgis.core import QgsProject, QgsVectorFileWriter
import os

# --- Configuration for the layer to export --- 
# Replace 'Your_Active_Layer_Name' with the actual name of the layer 
# you want to export from your QGIS project.
output_dir = r'C:\Users\183632\Desktop\GEO\2_Python_scripts_QGIS\Try'
layer_name_to_export = 'ACLED_distances_to_WAP_centroid' # Example: using one of the layers from your previous context

# --- Define the output path for the GeoJSON file --- 
# This will save to a temporary directory, similar to a local environment.
output_geojson_path = os.path.join(output_dir, 'ACLED_distances_to_WAP_centroid.geojson')

# --- Get the active layer from the QGIS project ---
layers = QgsProject.instance().mapLayersByName(layer_name_to_export)

if layers:
    qgis_layer_to_export = layers[0]
    print(f"Successfully retrieved layer '{qgis_layer_to_export.name()}' for export.")

    # --- Export the layer directly to GeoJSON ---
    # Options for QgsVectorFileWriter.writeAsVectorFormat:
    # 1. Layer to export
    # 2. Output path
    # 3. CRS (target_crs_id=0 for original CRS, or provide a QgsCoordinateReferenceSystem object)
    # 4. Driver name (e.g., 'GeoJSON', 'ESRI Shapefile', 'GPKG')
    # 5. Only selected features (False to export all)
    # 6. Options (e.g., 'ENCODING=UTF-8')

    # Use QgsProject.instance().transformContext() for writing transformations
    # QgsVectorFileWriter.writeAsVectorFormat also automatically handles projection if a target_crs is specified.

    # Example of exporting, preserving the original CRS of the layer
    error = QgsVectorFileWriter.writeAsVectorFormat(
        qgis_layer_to_export,
        output_geojson_path,
        'UTF-8', # Encoding
        qgis_layer_to_export.crs(), # Use the layer's own CRS
        'GeoJSON' # Driver name
    )

    if error == QgsVectorFileWriter.NoError:
        print(f"Successfully exported '{layer_name_to_export}' to GeoJSON: {output_geojson_path}")
        print("You can now open this GeoJSON file in QGIS.")
    else:
        print(f"Error exporting layer: {error}")
else:
    print(f"Error: Layer '{layer_name_to_export}' not found in QGIS project. Cannot export.")