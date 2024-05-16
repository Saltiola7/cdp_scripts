import csv
import json
import io

input_path = '/Users/tis/foam/cdp/data/turo.csv'
output_path = '/Users/tis/foam/cdp/data/turo.json'

data = []

with open(input_path, 'r', encoding='utf-8-sig') as file:
    reader = csv.DictReader(io.TextIOWrapper(file, newline='', encoding='utf-8'))
    for row in reader:
        data.append(dict(row))

with open(output_path, 'w', encoding='utf-8') as file:
    json.dump(data, file, indent=4)