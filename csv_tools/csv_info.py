import pandas as pd

# Specify the path to your CSV file
csv_file_path = '/Users/tis/foam/cdp/data/apollobusinesscenter.leads_web.csv'

# Read the CSV file, assuming the first row contains headers
df = pd.read_csv(csv_file_path)

# Print general information about the CSV file
print("General Information about the CSV File:")
print(df.info())

# Print the first few rows to get a sense of the data
print("\nPreview of the Data:")
print(df.head())
