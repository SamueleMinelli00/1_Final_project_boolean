#points paths
WDPA_path_points_0=r"C:\Users\183632\Desktop\GEO\0_GIS_Data\Protected Areas\WDPA_Apr2026_Public_shp\WDPA_Apr2026_Public_shp_0\WDPA_Apr2026_Public_shp-points.shp"
WDPA_path_points_1=r"C:\Users\183632\Desktop\GEO\0_GIS_Data\Protected Areas\WDPA_Apr2026_Public_shp\WDPA_Apr2026_Public_shp_1\WDPA_Apr2026_Public_shp-points.shp"
WDPA_path_points_2=r"C:\Users\183632\Desktop\GEO\0_GIS_Data\Protected Areas\WDPA_Apr2026_Public_shp\WDPA_Apr2026_Public_shp_2\WDPA_Apr2026_Public_shp-points.shp"

#polygons paths
WDPA_path_poly_0=r"C:\Users\183632\Desktop\GEO\0_GIS_Data\Protected Areas\WDPA_Apr2026_Public_shp\WDPA_Apr2026_Public_shp_0\WDPA_Apr2026_Public_shp-polygons.shp"
WDPA_path_poly_1=r"C:\Users\183632\Desktop\GEO\0_GIS_Data\Protected Areas\WDPA_Apr2026_Public_shp\WDPA_Apr2026_Public_shp_1\WDPA_Apr2026_Public_shp-polygons.shp"
WDPA_path_poly_2=r"C:\Users\183632\Desktop\GEO\0_GIS_Data\Protected Areas\WDPA_Apr2026_Public_shp\WDPA_Apr2026_Public_shp_2\WDPA_Apr2026_Public_shp-polygons.shp"

#upload WDPA layers
WDPA_path_points_0= iface.addVectorLayer (WDPA_path_points_0, "WDPA_points_0", "ogr")
WDPA_path_points_1= iface.addVectorLayer (WDPA_path_points_1, "WDPA_points_1", "ogr")
WDPA_path_points_2= iface.addVectorLayer (WDPA_path_points_2, "WDPA_points_2", "ogr")

WDPA_path_poly_0= iface.addVectorLayer (WDPA_path_poly_0, "WDPA_poly_0", "ogr")
WDPA_path_poly_1= iface.addVectorLayer (WDPA_path_poly_1, "WDPA_poly_1", "ogr")
WDPA_path_poly_2= iface.addVectorLayer (WDPA_path_poly_2, "WDPA_poly_2", "ogr")


#Merge them into a single WDPA layer


#Upload concerned countries shapefile

#Filter them per area (only BF; GH; TG; BJ; NE)