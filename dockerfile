# Usar una imagen base de Python
FROM python:3.11.8-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar el archivo de requerimientos al contenedor
COPY requirements.txt ./

# Actualizar pip e instalar las dependencias del proyecto
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar el resto de la aplicación al contenedor
COPY . .

# Exponer el puerto en el que la aplicación Flask correrá
EXPOSE 5000

# Configurar la variable de entorno para indicar el módulo y función de Flask
ENV FLASK_APP=src:init_app

# Comando para ejecutar la aplicación Flask
CMD ["flask", "run", "--host=0.0.0.0"]
