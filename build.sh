#!/usr/bin/env bash
# Exit on error
set -o errexit
pip install --upgrade pip

poetry install
# pip install -r requirements.txt
pip install --force-reinstall -U setuptools
# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate

if [[ $CREATE_SUPERUSER ]];
then
  python manage.py createsuperuser --no-input
fi
