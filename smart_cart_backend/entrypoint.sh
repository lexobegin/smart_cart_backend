#!/bin/bash

# Esperar a que la base de datos esté lista
echo "Esperando a la base de datos..."
until nc -z $DB_HOST $DB_PORT; do
  sleep 1
done

echo "Base de datos disponible. Aplicando migraciones..."
python manage.py migrate

echo "Arrancando servidor Django..."
gunicorn smart_cart_backend.wsgi:application --bind 0.0.0.0:8080
