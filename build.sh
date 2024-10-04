#!/usr/bin/env bash
# Exit on error
set -o errexit
pip install --upgrade pip

poetry install
pip install --force-reinstall -U setuptools
# Convert static asset files
python manage.py collectstatic --no-input

python manage.py migrate

if [[ $CREATE_SUPERUSER ]];
then
  python manage.py createsuperuser --no-input
fi
