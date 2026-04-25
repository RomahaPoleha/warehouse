FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc postgresql-client && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# ✅ СОЗДАЙ ПАПКУ ДЛЯ СТАТИКИ
RUN mkdir -p /app/staticfiles

# ✅ СОБЕРИ СТАТИКУ
RUN python manage.py collectstatic --noinput --clear

EXPOSE 8000

CMD ["gunicorn", "warehouse.wsgi:application", "--bind", "0.0.0.0:8000"]