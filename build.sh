#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

# Создаём папку для статики
mkdir -p staticfiles

# Собираем статику
python manage.py collectstatic --noinput

# === ПРИМЕНЯЕМ МИГРАЦИИ (ОБЯЗАТЕЛЬНО!) ===
python manage.py migrate --noinput

# === СОЗДАЁМ СУПЕРПОЛЬЗОВАТЕЛЯ ===
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin123')"