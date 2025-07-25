#!/bin/bash
set -e

echo "Extrayendo host y puerto desde DATABASE_URL..."
export DB_HOST=$(echo $DATABASE_URL | sed -E 's|.*://[^@]+@([^:/]+):([0-9]+).*|\1|')
export DB_PORT=$(echo $DATABASE_URL | sed -E 's|.*://[^@]+@([^:/]+):([0-9]+).*|\2|')

echo "Esperando a la base de datos en $DB_HOST:$DB_PORT..."
for i in {1..60}; do
  nc -z "$DB_HOST" "$DB_PORT" && break
  echo "Esperando... ($i/60)"
  sleep 1
done

# Si no se pudo conectar después de 60 segundos
if ! nc -z "$DB_HOST" "$DB_PORT"; then
  echo "No se pudo conectar a la base de datos en 60 segundos."
  exit 1
fi

echo "Base de datos disponible. Aplicando migraciones..."
python manage.py migrate

echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo "Arrancando servidor Django en puerto 10000..."
gunicorn smart_cart_backend.wsgi:application --bind 0.0.0.0:10000

