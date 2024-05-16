import pandas as pd
import os

def transform_csv(input_file_path):
    # Load the CSV file
    df = pd.read_csv(input_file_path)

    # Delete the specified columns
    df.drop(['Target', 'Target Type', 'Database', 'Summary'], axis=1, inplace=True)

    # Melting the dataframe to transform it
    df_melted = df.melt(id_vars=['Metric'], var_name='Date', value_name='Value')

    # Pivot the data to get the desired structure
    df_pivot = df_melted.pivot(index='Date', columns='Metric', values='Value')
    df_pivot.reset_index(inplace=True)

    # Return the transformed dataframe
    return df_pivot