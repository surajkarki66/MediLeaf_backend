#!/bin/sh

python manage.py makemigrations
python manage.py migrate --no-input
python manage.py collectstatic --no-input
python manage.py loaddata --app account initial_data
python manage.py loaddata --app plant initial_data

gunicorn MediLeaf_backend.wsgi:application --bind 0.0.0.0:8000