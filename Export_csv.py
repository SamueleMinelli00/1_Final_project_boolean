from main import ACLED_to_WAP_clean
import pandas as pd

 #Exporting ACLED_to_WAP_clean as CSV
output_path = r'C:\Users\183632\OneDrive\Culture\0-UNI\2025-26_Boolean\Data Analytics\6_Final project\1_Final_project_boolean\Data\ACLED_to_WAP_clean.csv'
ACLED_to_WAP_clean.to_csv(output_path, index=False)
print(f"\nACLED_to_WAP_clean exportd to CSV at: {output_path}")

# print(ACLED_to_WAP_clean.head(5))
# print(ACLED_to_WAP_clean.info())