import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import CSV_pivot

# Path to the input CSV file
input_file_path = 'SEO/Semrush/seedsoflove/seeds_of_love-overview-trend-2023-12-16T02_46_19Z.csv'

# Call the function and assign the return value to df
df = CSV_pivot.transform_csv(input_file_path)
print(df)

# Ensure 'Date' is a datetime object and sort data
df['Date'] = pd.to_datetime(df['Date'])
df.sort_values('Date', inplace=True)

# Plot
sns.set(style="whitegrid")
plt.figure(figsize=(12, 8))

# Plotting Traffic Data
sns.lineplot(data=df, x='Date', y='Organic Traffic', color='#7fb86e', label='Seeds of Love')

# Additional Plot Settings
plt.gca().xaxis.set_major_locator(mdates.YearLocator())
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
plt.xticks(rotation=45)
plt.grid(visible=False)

# Renaming axis titles
plt.xlabel("Vuosi")
plt.ylabel("Liikenne")

# Setting the legend to a lower position within the plot
plt.legend(loc=(0.1, 0.1))  # Adjust these values as needed

plt.gca().set_facecolor('none')
plt.gca().figure.set_facecolor('none')
sns.despine(left=True)

# Save the plot
save_path = '/Users/tis/Dendron/notes/SEO/Semrush/seedsoflove'
plt.savefig(save_path, dpi=2000, bbox_inches='tight', transparent=True)