#!/bin/bash

# Path to your Python script
APP_PATH="weatherAppUI_v2.py"

# Activate virtual environment if needed
# source /path/to/venv/bin/activate

while true; do
    echo "[$(date)] Running weather UI..."
    ./bin/python3 "$APP_PATH"
    echo "[$(date)] App closed. Waiting 1 hour..."
    sleep 3600  # 1 hour = 3600 seconds
done

