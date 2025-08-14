#!/bin/bash

echo "Running connection test in container..."
docker exec python_dev python scripts/run_container.py connection_test
