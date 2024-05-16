import pandas as pd
import os

# Define the input and output file paths
input_file_path = 'dev/KatiesBUMPERS/ubersuggest site audit katiesbumpers.com/low_word_count.csv'
output_directory = 'code/function/seo/data/out/custom_search'
output_file_path = os.path.join(output_directory, 'filtered_products.csv')

# Create output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Read the existing CSV file
try:
    df = pd.read_csv(input_file_path)
except FileNotFoundError:
    print(f"File not found at path: {input_file_path}")
    exit()

# Filter out the rows with '/products/' in the URL
filtered_df = df[df['Url'].str.contains('/products/')]

# Write the filtered DataFrame to a new CSV file
filtered_df.to_csv(output_file_path, index=False)

print(f"Successfully filtered and saved to {output_file_path}")
