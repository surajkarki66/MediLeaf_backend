#!/bin/bash

# Build the project
echo "Building the project..."
python3.11.3 -m pip install -r requirements.txt

echo "Make Migration..."
python3.11.3 manage.py makemigrations --noinput
python3.11.3 manage.py migrate --noinput

echo "Collect Static..."
python3.11.3 manage.py collectstatic --noinput --clear