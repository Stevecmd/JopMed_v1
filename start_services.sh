#!/bin/bash

# Function to kill all background processes
cleanup() {
    echo "Cleaning up..."
    pkill -P $$
    exit 0
}

# Trap SIGINT (Ctrl+C) and call the cleanup function
trap cleanup SIGINT

# Start the API in the background
JOPMED_MYSQL_USER=jopmed_dev \
JOPMED_MYSQL_PWD=jopmed_dev_pwd \
JOPMED_MYSQL_HOST=localhost \
JOPMED_MYSQL_DB=jopmed_dev_db \
JOPMED_TYPE_STORAGE=db \
JOPMED_API_HOST=0.0.0.0 \
JOPMED_API_PORT=5000 \
python3 -m api.v1.app &

# Start the web application in the foreground
JOPMED_MYSQL_USER=jopmed_dev \
JOPMED_MYSQL_PWD=jopmed_dev_pwd \
JOPMED_MYSQL_HOST=localhost \
JOPMED_MYSQL_DB=jopmed_dev_db \
JOPMED_TYPE_STORAGE=db \
JOPMED_API_HOST=0.0.0.0 \
JOPMED_API_PORT=5000 \
python3 -m web_dynamic.jopmed

# Wait for background jobs to complete (if needed)
wait
