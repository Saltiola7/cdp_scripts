# data_sanitizer.py
import pandas as pd

def sanitize_column_names(columns):
    return (
        columns
        .str.lower()  # convert to lowercase
        .str.replace(r'[^\w\s]', '_', regex=True)  # replace non-alphanumeric characters with underscores
        .str.replace(r'__+', '_', regex=True)  # replace multiple underscores with single underscore
        .str.strip('_')  # remove leading and trailing underscores
        .str.replace(r'^(\d+)', r'_\1', regex=True)  # prefix numeric column names with an underscore
    )