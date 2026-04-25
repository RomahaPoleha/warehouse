#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
# Создаём папку ДО collectstatic:
mkdir -p staticfiles
python manage.py collectstatic --noinput
python manage.py migrate