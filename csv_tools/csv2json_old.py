import csv
import json

def csv_to_json(csv_file_path, json_file_path):
    data = []

    with open(csv_file_path, 'r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            cleaned_row = {key.strip().replace('"', ''): value.strip() for key, value in row.items()}
            data.append(cleaned_row)

    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=2, separators=(',', ':'), ensure_ascii=False)

# Usage example
csv_file_path = '/Users/tis/foam/cdp/data/turo.csv'
json_file_path = '/Users/tis/foam/cdp/data/turo.json'
csv_to_json(csv_file_path, json_file_path)
