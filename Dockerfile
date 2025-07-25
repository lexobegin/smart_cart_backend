# Imagen base de Python
FROM python:3.11-slim

# Variables de entorno para evitar errores de entrada
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Crear directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update \
    && apt-get install -y netcat gcc postgresql-client libpq-dev \
    && apt-get clean

# Copiar dependencias
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del proyecto
COPY . .

# Ejecutar collectstatic (archivos estáticos)
RUN python manage.py collectstatic --noinput

# Exponer el puerto en que se ejecutará
EXPOSE 10000

# Agregar script de inicio para esperar a la BD (opcional)
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Comando de inicio
ENTRYPOINT ["/entrypoint.sh"]
