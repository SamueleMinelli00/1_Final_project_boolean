
from main import ACLED_to_WAP_clean
import pandas as pd
import sys

# Exporting `ACLED_to_WAP_clean` as CSV and XLSX
csv_output_path = r'C:\Users\183632\OneDrive\Culture\0-UNI\2025-26_Boolean\Data Analytics\6_Final project\1_Final_project_boolean\Data\ACLED_to_WAP_clean.csv'
xlsx_output_path = r'C:\Users\183632\OneDrive\Culture\0-UNI\2025-26_Boolean\Data Analytics\6_Final project\1_Final_project_boolean\Data\ACLED_to_WAP_clean.xlsx'

ACLED_to_WAP_clean.to_csv(csv_output_path, index=False)
ACLED_to_WAP_clean.to_excel(xlsx_output_path, index=False)

print(f"\nACLED_to_WAP_clean exported to CSV at: {csv_output_path}")
print(f"ACLED_to_WAP_clean exported to XLSX at: {xlsx_output_path}")

# print(ACLED_to_WAP_clean.head(5))
# print(ACLED_to_WAP_clean.info())