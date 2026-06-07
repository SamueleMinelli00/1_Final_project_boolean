import os

base_folder = r"C:\Users\183632\Desktop\GEO\0_GIS_Data\Protected Areas\WDPA_Apr2026_Public_shp"

num_files = 3

#lists to store the file paths
wdpa_point_paths = []
wdpa_poly_paths = []

#constructing paths dynamically
for i in range(num_files):
    point_path = os.path.join(base_folder, f"WDPA_Apr2026_Public_shp_{i}", "WDPA_Apr2026_Public_shp-points.shp")
    poly_path = os.path.join(base_folder, f"WDPA_Apr2026_Public_shp_{i}", "WDPA_Apr2026_Public_shp-polygons.shp")
    wdpa_point_paths.append(point_path)
    wdpa_poly_paths.append(poly_path)
    
#Upload WDPA layers using loops
loaded_point_layers =[]
loaded_poly_layers =[]

#points
for i, path in enumerate(wdpa_point_paths):
    layer_name = f"WDPA_points_{i}"
    vlayer = iface.addVectorLayer(path, layer_name, "ogr")
    if vlayer:
        loaded_point_layers.append(vlayer)
        print(f"Loaded point layer: {layer_name}")
    else:
        print(f"Failed to load point layer: {layer_name} from {path}")
        
#poly
for i, path in enumerate(wdpa_poly_paths):
    layer_name = f"WDPA_poly_{i}"
    vlayer = iface.addVectorLayer(path, layer_name, "ogr")
    if vlayer:
        loaded_poly_layers.append(vlayer)
        print(f"Loaded point layer: {layer_name}")
    else:
        print(f"Failed to load point layer: {layer_name} from {path}")
        
