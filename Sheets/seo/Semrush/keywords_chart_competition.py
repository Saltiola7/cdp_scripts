import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# List of CSV files
csv_files = [
    '/Users/tis/Dendron/notes/SEO/Hamppufarmi exports/All data/sr_kw_traffic_hamppufarmi.csv',
    '/Users/tis/Dendron/notes/SEO/Hamppufarmi exports/All data/sr_kw_traffic_hamppumaa.csv',
    '/Users/tis/Dendron/notes/SEO/Hamppufarmi exports/All data/sr_kw_traffic_impolan.csv'
]

# List to store the data
data = []

# Process each CSV file
for filename in csv_files:
    # Load the CSV file into a DataFrame
    df = pd.read_csv(filename)
    
    # Ensure 'Date' is a datetime object and sort data
    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values('Date', inplace=True)
    
    # Extract the row with the latest date
    latest_row = df[df['Date'] == df['Date'].max()]
    
    # Extract the 'Yritys' and 'Organic Keywords' values
    if 'hamppufarmi' in filename:
        yritys = 'Hamppufarmi'
    elif 'hamppumaa' in filename:
        yritys = 'Hamppumaa'
    elif 'impolan' in filename:
        yritys = 'Impolan Kasvitila'
    else:
         yritys = 'Unknown'
        
    organic_keywords = latest_row['Organic Keywords'].values[0]
    
    # Add the data to the list
    data.append([yritys, organic_keywords])

# Create a DataFrame with the data
df = pd.DataFrame(data, columns=['Yritys', 'Organic Keywords'])

# Plot
sns.set(style="whitegrid")
plt.figure(figsize=(12, 8))

# Plotting Organic Keywords Data
barplot = sns.barplot(data=df, x='Yritys', y='Organic Keywords')

# Additional Plot Settings
plt.grid(visible=False)

# Renaming axis titles
plt.ylabel("Avainsanat")

plt.gca().set_facecolor('none')
plt.gca().figure.set_facecolor('none')
sns.despine(left=True)

# Adding the text labels for each bar
for p in barplot.patches:
    barplot.annotate(format(p.get_height(), '.0f'), 
                     (p.get_x() + p.get_width() / 2., p.get_height()), 
                     ha = 'center', va = 'center', 
                     xytext = (0, 10), 
                     textcoords = 'offset points')

# Save the plot
save_path = '/Users/tis/Dendron/notes/assets/proposals/Hamppufarmi/keywords_comparison.png'
plt.savefig(save_path, dpi=2000, bbox_inches='tight', transparent=True)

plt.show()