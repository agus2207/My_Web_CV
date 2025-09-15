# Usar una imagen base de Python oficial
FROM python:3.12-buster

# Establecer el directorio de trabajo en /app
WORKDIR /app

# Copiar el archivo de dependencias y luego instalarlas
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

# Copiar el resto del código de la aplicación
COPY . .

# Comando para ejecutar la aplicación
CMD ["python3", "app.py"]
