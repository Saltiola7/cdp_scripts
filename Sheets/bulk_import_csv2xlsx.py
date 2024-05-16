import pandas as pd
import os

def csv_to_xlsx(directory_path, output_file):
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        for filename in os.listdir(directory_path):
            if filename.endswith('.csv'):
                file_path = os.path.join(directory_path, filename)
                df = pd.read_csv(file_path)
                # Truncate sheet name to 31 characters
                sheet_name = os.path.splitext(filename)[0][:31]
                df.to_excel(writer, sheet_name=sheet_name, index=False)

# Usage
directory_path = 'YOUR_PATH'
output_file = 'YOUR_PATH'
csv_to_xlsx(directory_path, output_file)