# Usa una imagen base ligera con Python
FROM python:3.13-slim

# Variables de entorno para mejorar el rendimiento
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Crea y usa el directorio de trabajo
WORKDIR /app

# Copia e instala las dependencias
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Instala Gunicorn adicionalmente (si no está en requirements.txt)
RUN pip install gunicorn

# Copia el resto del proyecto al contenedor
COPY . .

# Expone el puerto 8000
EXPOSE 8000

# Comando para iniciar el servidor usando Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "HydroSys.wsgi:application"]
