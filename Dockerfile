# Usar una imagen base de Python oficial
FROM python:3.12

# Establecer el directorio de trabajo en /app
WORKDIR /app

# Copiar el archivo de dependencias y luego instalarlas
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

# Copiar el resto del código de la aplicación
COPY . .

# Expón el puerto que Gunicorn usará
EXPOSE 8080

# Comando para ejecutar la aplicación
# CMD ["python3", "app.py"]
# CMD ["gunicorn", "app:server", "--bind", "0.0.0.0:8080", "--workers", "2"]
CMD ["gunicorn", "app:server", "--bind", "0.0.0.0:8080", "--workers", "1", "--threads", "4", "--timeout", "0"]
