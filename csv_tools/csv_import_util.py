import pandas as pd
from sqlalchemy import create_engine, inspect
from prefect import task

def infer_schema(df):
    """
    Infer the SQL data types from a pandas DataFrame.
    """
    # Mapping from pandas dtype to SQL data types
    dtype_map = {
        'int64': 'INTEGER',
        'float64': 'FLOAT',
        'bool': 'BOOLEAN',
        'object': 'TEXT',  # Defaulting object types to TEXT
        # Add more mappings as necessary
    }
    column_types = {col: dtype_map[str(dtype)] for col, dtype in df.dtypes.items()}
    return column_types

def create_table_if_not_exists(engine, table_name, schema):
    """
    Create a PostgreSQL table based on the inferred schema if it does not exist.
    """
    if not inspect(engine).has_table(table_name):
        columns_sql = ', '.join([f"{col} {dtype}" for col, dtype in schema.items()])
        sql_statement = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_sql});"
        with engine.connect() as conn:
            conn.execute(sql_statement)
        print(f"Table {table_name} created with schema: {schema}")
    else:
        print(f"Table {table_name} already exists.")

@task
def import_csv_to_postgresql(csv_path, db_connection_string, table_name):
    """
    Task to import CSV data into a PostgreSQL table, creating the table dynamically if it does not exist.
    """
    # Read CSV file into DataFrame
    df = pd.read_csv(csv_path)
    
    # Create SQLAlchemy engine
    engine = create_engine(db_connection_string)
    
    # Infer schema and create table if it does not exist
    schema = infer_schema(df)
    create_table_if_not_exists(engine, table_name, schema)
    
    # Append DataFrame to PostgreSQL table
    df.to_sql(table_name, engine, if_exists='append', index=False)
    print(f"Data imported successfully into {table_name}")