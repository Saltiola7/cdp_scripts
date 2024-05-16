import pandas as pd

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
    
    # Extract the row with the latest date
    latest_row = df[df['Date'] == df['Date'].max()]  # Replace 'Date' with the actual column name for the date in your CSV files
    
    # Extract the 'Yritys', 'Organic Traffic', and 'Paid Traffic' values
    if 'hamppufarmi' in filename:
        yritys = 'Hamppufarmi'
    elif 'hamppumaa' in filename:
        yritys = 'Hamppumaa'
    elif 'impolan' in filename:
        yritys = 'Impolan Kasvitila'
    else:
        yritys = 'Unknown'
        
    maksettu = latest_row['Paid Traffic'].values[0]
    orgaaninen = latest_row['Organic Traffic'].values[0]
    
    # Add the data to the list
    data.append([yritys, maksettu, orgaaninen])

# Create a DataFrame with the data
df = pd.DataFrame(data, columns=['Yritys', 'Maksettu', 'Orgaaninen'])

# Find the row for 'Hamppufarmi'
hamppufarmi_row = df[df['Yritys'] == 'Hamppufarmi']

# Extract the 'Orgaaninen' value for 'Hamppufarmi'
hamppufarmi_orgaaninen = hamppufarmi_row['Orgaaninen'].values[0]

# Create a new column 'Orgaaninen X'
df['Orgaaninen X'] = df.apply(lambda row: None if row['Yritys'] == 'Hamppufarmi' else round(row['Orgaaninen'] / hamppufarmi_orgaaninen), axis=1)

# Convert the DataFrame to a Markdown table
markdown_table = df.to_markdown(index=False)

# Print the Markdown table
print(markdown_table)