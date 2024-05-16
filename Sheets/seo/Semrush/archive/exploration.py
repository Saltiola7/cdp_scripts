import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Directory containing the transformed CSV files
directory = '/Users/tis/Dendron/notes/SEO/Hamppu-suomi'

def plot_charts(directory):
    for filename in os.listdir(directory):
        if filename.startswith('transformed_') and filename.endswith('.csv'):
            file_path = os.path.join(directory, filename)
            df = pd.read_csv(file_path)
            df['Date'] = pd.to_datetime(df['Date'])  # Convert 'Date' to datetime for better plotting

            # Plot each metric over time
            for column in df.columns[1:]:
                plt.figure(figsize=(10, 6))
                sns.lineplot(data=df, x='Date', y=column)
                plt.title(f'{column} over Time for {filename}')
                plt.xlabel('Date')
                plt.ylabel(column)
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.show()

# Call the function
plot_charts(directory)
