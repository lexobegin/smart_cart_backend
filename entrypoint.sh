#!/bin/bash
set -e

echo "Esperando a la base de datos..."
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

echo "Arrancando servidor Django..."
gunicorn smart_cart_backend.wsgi:application --bind 0.0.0.0:8080
