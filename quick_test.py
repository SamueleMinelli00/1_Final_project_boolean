try:
    from permutations_years import results_gdf
    print("SUCCESS: Import worked")
    print(f"Type: {type(results_gdf)}")
    print(f"Shape: {results_gdf.shape}")
    results_gdf.to_excel('test.xlsx', index=False)
    print("SUCCESS: Export worked")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
