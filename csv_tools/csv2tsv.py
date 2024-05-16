import time
from typing import TextIO

def convert_csv_to_tsv(input_file: TextIO, output_file: TextIO) -> None:
    """
    Converts a CSV file to a TSV file, line by line.

    Args:
        input_file (TextIO): The input CSV file opened in text mode.
        output_file (TextIO): The output TSV file opened in text mode.
    """
    start_time = time.time()  # Record the start time

    for line in input_file:
        # Replace double-quoted fields with tab-separated fields
        tsv_line = line.replace('","', "\t").replace('"', '')
        output_file.write(tsv_line)

    end_time = time.time()  # Record the end time
    elapsed_time = end_time - start_time
    print(f"Conversion took {elapsed_time:.6f} seconds.")

if __name__ == "__main__":
    input_path = "/Users/tis/foam/cdp/data/turo.csv"
    output_path = "/Users/tis/foam/cdp/data/turo_python.tsv"

    with open(input_path, "r") as input_file, open(output_path, "w") as output_file:
        convert_csv_to_tsv(input_file, output_file)