#!/bin/zsh

# Path to the data directory you want to monitor
DATA_DIR="/Users/tis/foam/cdp/data"

# Database connection details
DB_NAME="db"
DB_USER="postgres"
DB_PASSWORD="mysecretpassword"  # Specify the database password here
CONTAINER_NAME="cdp-postgres-1"  # Name or ID of your PostgreSQL Docker container

# Function to handle new files
handle_new_file() {
  local filename=$1
  local filepath="$DATA_DIR/$filename"
  # Generate current timestamp in the format PostgreSQL expects (YYYY-MM-DD HH:MI:SS)
  local timestamp=$(date '+%Y-%m-%d %H:%M:%S')

  # Insert the file details into the database, ignoring duplicates based on filename
  # Adjusted to run psql inside the Docker container
  docker exec $CONTAINER_NAME psql -U $DB_USER -d $DB_NAME -c \
    "INSERT INTO log.import (filename, filepath, timestamp) VALUES ('$filename', '$filepath', '$timestamp') ON CONFLICT (filename) DO NOTHING;" > /dev/null 2>&1
}

# Export function so it's available to subshells spawned by fswatch
export -f handle_new_file

# Start monitoring the directory and handle new files
fswatch "$DATA_DIR" | while read file; do
  # Ensure that only file events are processed
  if [[ -f "$file" ]]; then
    handle_new_file "$(basename "$file")"
  fi
done