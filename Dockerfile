# Imagen base de Python
FROM python:3.11-slim

# Variables de entorno para evitar archivos pyc y mejorar logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema (incluyendo netcat-openbsd)
RUN apt-get update && \
    apt-get install -y netcat-openbsd gcc postgresql-client libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el proyecto
COPY . .

# Generar archivos estáticos (si aplica)
RUN python manage.py collectstatic --noinput

# Exponer el puerto que Render espera
EXPOSE 10000

# Copiar el script de inicio y darle permisos
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Comando de arranque
ENTRYPOINT ["/entrypoint.sh"]
