#!/usr/bin/env zsh

# Check if the required argument (input CSV file) is provided
if [[ $# -ne 1 ]]; then
    echo "Usage: $0 <input_csv_file>"
    exit 1
fi

# Define the input CSV file from the first script argument
input_file="$1"

# Define the output JSON file, replacing the CSV extension with JSON
output_file="${input_file%.csv}.json"

# Read the CSV header row to determine the JSON keys
header_row=$(head -n 1 "$input_file")
IFS=',' read -r -A header_fields <<< "$header_row"

# Create an empty array to store the JSON objects
json_objects=()

# Read the CSV data excluding the header row
tail -n +2 "$input_file" | while IFS= read -r line; do
    IFS=',' read -r -A row_fields <<< "$line"
    row_json="{"

    # Loop through each header field to construct the JSON object from CSV data
    for i in {1..${#header_fields[@]}}; do
        key="${header_fields[$i]}"
        value="${row_fields[$i]}"

        # Escape any double quotes, backslashes, and newlines in the value
        value="${value//\"/\\\"}"
        value="${value//\\/\\\\}"
        value="${value//$'\n'/\\n}"
        value="${value//$'\r'/\\r}"

        # Trim leading/trailing whitespace from the value
        value="${value#"${value%%[![:space:]]*}"}"
        value="${value%"${value##*[![:space:]]}"}"

        # Add the key-value pair to the JSON object
        row_json+="\"$key\":\"$value\","
    done

    # Remove the trailing comma from the JSON object and close it
    row_json="${row_json%,}}"

    # Append the complete JSON object to the array
    json_objects+=("$row_json")
done

# Combine all JSON objects into a JSON array
json_array="[${(j:,:)json_objects}]"
echo "$json_array" > "$output_file"  # Write the JSON array to the output file

# Print a confirmation message with the output file path
echo "CSV file converted to JSON: $output_file"