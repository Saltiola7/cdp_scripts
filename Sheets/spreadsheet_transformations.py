import openpyxl

# Path to your Excel file
file_path = '/Users/tis/foam/cdp/function/seo/Semrush/archive/Hamppu-suomi/Hamppufarmi SEO.xlsx'
sheet_name = 'sf_issues'

# Load the workbook and select the specified sheet
workbook = openpyxl.load_workbook(file_path)
sheet = workbook[sheet_name]
cs
# Define the mapping for Issue Priority
priority_mapping = {'High': 1, 'Medium': 2, 'Low': 3}

# Column index for "Issue Priority" (3rd column, so index is 2)
issue_priority_col_index = 2

# Iterate through rows starting from row 2 (since row 1 has headers) and update the 'Issue Priority' column
for row in sheet.iter_rows(min_row=2):
    issue_priority_cell = row[issue_priority_col_index]
    # Apply mapping, and if value is not in mapping, keep it as it is
    issue_priority_cell.value = priority_mapping.get(issue_priority_cell.value, issue_priority_cell.value)

# Save the workbook
workbook.save(file_path)

print("Excel file updated with priority mappings and other sheets preserved.")
