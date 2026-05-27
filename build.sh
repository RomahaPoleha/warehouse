#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

# Создаём папку для статики
mkdir -p staticfiles

# Собираем статику
python manage.py collectstatic --noinput

# === ПРИМЕНЯЕМ МИГРАЦИИ (ОБЯЗАТЕЛЬНО!) ===
python manage.py migrate --noinput

