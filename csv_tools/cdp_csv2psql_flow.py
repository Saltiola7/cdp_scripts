from prefect import Flow, task
from function.data.csv_import_util import import_csv_to_postgresql
from function.util.file_monitor import start_monitoring
import threading

# Define your database connection string
db_connection_string = 'localhost'

# Define the PostgreSQL table name dynamically based on file path
# Placeholder function, actual logic to be implemented based on file path
def get_table_name_from_file_path(file_path):
    parts = file_path.split('/')
    client_name = parts[2]  # Adjust index based on your path structure
    data_source = parts[3]  # Adjust index based on your path structure
    table_name = f"{client_name}.{data_source}"
    return table_name

@task
def process_file(csv_path, db_connection_string):
    table_name = get_table_name_from_file_path(csv_path)
    import_csv_to_postgresql(csv_path=csv_path, db_connection_string=db_connection_string, table_name=table_name)
    print(f"Data imported successfully into {table_name}")

def on_file_created(file_path):
    print(f"New file detected: {file_path}")
    # Trigger the Prefect flow here
    with Flow("CSV to PostgreSQL Import") as flow:
        process_file(csv_path=file_path, db_connection_string=db_connection_string)
    flow.run()

if __name__ == "__main__":
    path_to_monitor = 'data/'

    # Start the file monitoring in a separate thread to not block the main thread
    monitor_thread = threading.Thread(target=start_monitoring, args=(path_to_monitor, on_file_created))
    monitor_thread.start()

    # Keep the script running to listen for file events
    monitor_thread.join()