#FROM python:3.11-slim
#
#WORKDIR /app
#
## Системные зависимости
#RUN apt-get update && apt-get install -y \
#    gcc \
#    postgresql-client \
#    && rm -rf /var/lib/apt/lists/*
#
## Python зависимости
#COPY requirements.txt .
#RUN pip install --no-cache-dir -r requirements.txt
#
## Код проекта
#COPY . .
#
## Папка для статики
#RUN mkdir -p /app/staticfiles
#
## Собираем статику
#RUN python manage.py collectstatic --noinput --clear
#
## Порт
#EXPOSE 8000
#
## Запуск
#CMD ["gunicorn", "warehouse.wsgi:application", "--bind", "0.0.0.0:80"]

FROM python:3.11-slim

WORKDIR /app

# Минимальные зависимости
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Порт 80 (важно для Amvera)
EXPOSE 80

# Запуск
CMD ["gunicorn", "warehouse.wsgi:application", "--bind", "0.0.0.0:80"]