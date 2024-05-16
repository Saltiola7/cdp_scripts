import pandas as pd
import os

def transform_csv(input_file_path, output_file_path):
    # Load the CSV file
    df = pd.read_csv(input_file_path)

    # Delete the specified columns
    df.drop(['Target', 'Target Type', 'Database', 'Summary'], axis=1, inplace=True)

    # Melting the dataframe to transform it
    df_melted = df.melt(id_vars=['Metric'], var_name='Date', value_name='Value')

    # Pivot the data to get the desired structure
    df_pivot = df_melted.pivot(index='Date', columns='Metric', values='Value')
    df_pivot.reset_index(inplace=True)

    # Save the transformed dataframe
    df_pivot.to_csv(output_file_path, index=False)

# Directories
input_directory = '/Users/tis/Dendron/notes/SEO/semrush export'
output_directory = '/Users/tis/Dendron/notes/SEO/SeedsOfLove/'

# Process each CSV file in the directory
for filename in os.listdir(input_directory):
    if filename.endswith('.csv'):
        input_file_path = os.path.join(input_directory, filename)
        output_file_path = os.path.join(output_directory, f'transformed_{filename}')
        transform_csv(input_file_path, output_file_path)
