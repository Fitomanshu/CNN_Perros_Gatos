# Usar Ubuntu 24.10 como base
FROM ubuntu:24.10

# Establecer el directorio de trabajo
WORKDIR /app

# Actualizar el sistema e instalar dependencias necesarias
RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Actualizar pip
#RUN python3 -m pip install --upgrade pip

# Instalar FastAPI y Uvicorn
#RUN apt-get update &&  apt-get install -y  python3-fastapi python3-uvicorn 
#RUN apt-get update &&  apt-get install -y python3.12-venv

#RUN python3 -m venv venvfast


# Copiar tu código de la aplicación (asumiendo que tengas un archivo main.py)
COPY ./app /app

# Exponer el puerto en el que correrá la aplicación
EXPOSE 8000

# Comando para ejecutar Uvicorn con FastAPI
CMD [ "bash" ]
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


# apt-get update
# apt install python3.12-venv
# python3 -m venv /venvfast
# python3 -m venv venvfast
# uvicorn main:app --host 0.0.0.0 --port 8000
# pip install pillow python-multipart