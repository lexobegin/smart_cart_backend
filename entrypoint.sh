#!/bin/bash
set -e

# Extraer host y puerto usando Python (más seguro y flexible)
echo "Extrayendo host y puerto desde DATABASE_URL con Python..."
DB_HOST=$(python3 -c "import os; from urllib.parse import urlparse; print(urlparse(os.environ['DATABASE_URL']).hostname)")
DB_PORT=$(python3 -c "import os; from urllib.parse import urlparse; print(urlparse(os.environ['DATABASE_URL']).port or 5432)")

echo "Host: $DB_HOST"
echo "Puerto: $DB_PORT"

echo "Esperando a la base de datos en $DB_HOST:$DB_PORT..."
for i in {1..60}; do
  nc -z "$DB_HOST" "$DB_PORT" && break
  echo "Esperando... ($i/60)"
  sleep 1
done

if ! nc -z "$DB_HOST" "$DB_PORT"; then
  echo "No se pudo conectar a la base de datos en 60 segundos."
  exit 1
fi

echo "Base de datos disponible. Aplicando migraciones..."
# python manage.py makemigrations core
python manage.py migrate

echo "Borrando todos los datos de la base de datos..."
python manage.py flush --noinput

echo "Poblando datos iniciales..."
python manage.py populate_user_db
python manage.py populate_producto_db

echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo "Arrancando servidor Django en puerto 10000..."
gunicorn smart_cart_backend.wsgi:application --bind 0.0.0.0:10000
