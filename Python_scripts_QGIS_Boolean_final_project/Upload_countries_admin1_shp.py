
import os

base_folder_countries = r"C:\Users\183632\Desktop\GEO\0_GIS_Data\0_Countries_Vectors\Map_files\Countries"
base_folder_admin1 = r"C:\Users\183632\Desktop\GEO\0_GIS_Data\0_Countries_Vectors\Map_files\Admin1"

#lists to store the file paths + iso
countries_iso = ['bf', 'bj', 'gh', 'ne', 'ng', 'tg']
countries_shp_paths = []
admin1_shp_paths = []

#constructing paths dyamically
for i in range(len(countries_iso)):
    countries_shp_path = os.path.join(base_folder_countries, f"{countries_iso[i]}.shp")
    countries_shp_paths.append(countries_shp_path)
    admin1_shp_path = os.path.join(base_folder_admin1, f"{countries_iso[i]}.shp")
    admin1_shp_paths.append(admin1_shp_path)

loaded_country_layers = []
loaded_admin1_layers = []

#uploading countries' vectors
for i, path in enumerate(countries_shp_paths):
    l_name = f"{countries_iso[i]}_boundary"
    vlayer = iface.addVectorLayer(path, l_name, "ogr")
    if vlayer:
        loaded_country_layers.append(vlayer)
        print(f"Loaded country layer: {l_name}")
    else:
        print(f"failed to load country layer: {l_name} from {path}")
        
#The shp file for BF_admin1 does not work --> I have done it manually
path=r"C:\Users\183632\Desktop\GEO\0_GIS_Data\0_Countries_Vectors\Map_files\BF\bfa_shp_admin1\bfa_admin1.shp"
bf_admin1_boundary = iface.addVectorLayer(path, "bf_admin1_boundary", "ogr")

#upoloading admin1 vectors
for i, path in enumerate(admin1_shp_paths):
    l_name = f"{countries_iso[i]}_admin1_boundary"
    vlayer = iface.addVectorLayer(path, l_name, "ogr")
    if vlayer:
        loaded_country_layers.append(vlayer)
        print(f"Loaded country layer: {l_name}")
    else:
        print(f"failed to load country layer: {l_name} from {path}")
    