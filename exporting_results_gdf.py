try:
    from permutations_years import results_gdf
    print("SUCCESS: Import worked")
    print(f"Type: {type(results_gdf)}")
    print(f"Shape: {results_gdf.shape}")
    xlsx_output_path_results_gdf = r'C:\Users\183632\OneDrive\Culture\0-UNI\2025-26_Boolean\Data Analytics\6_Final project\1_Final_project_boolean\Data\results_gdf.xlsx'
    results_gdf.to_excel(xlsx_output_path_results_gdf, index=False)
    print("SUCCESS: Export worked")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
