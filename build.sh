#!/usr/bin/env bash
# Exit on error
set -o errexit
pip install --upgrade pip

poetry install
pip install --force-reinstall -U setuptools
# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate

pip install 'git+https://github.com/SKTBrain/KoBERT.git#egg=kobert_tokenizer&subdirectory=kobert_hf'