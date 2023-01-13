# Mlflow-docker-compose
1. Build dockerfile
2. Set .env file for docker-compose
3. Run "docker-compose up -d"

# mlflow dockerfile
``` docker
FROM continuumio/miniconda3:latest
WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y git
RUN pip install mlflow psycopg2-binary pymysql boto3

RUN cd /app && git clone https://github.com/mlflow/mlflow-example.git

COPY wait-for-it.sh wait-for-it.sh

RUN chmod +x wait-for-it.sh
```

# docker-compose

``` yaml
version: "3.3"
services:
  db:
    container_name: mlflow-db
    image: postgres:latest
    restart: always
    expose:
      - ${DB_PORT}
    environment:
      - POSTGRES_DB=${DB_NAME}
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PW}
      - TZ=Asia/Seoul
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -d $${POSTGRES_DB} -U $${POSTGRES_USER}" ]
      interval: 15s
      timeout: 10s
      retries: 5
    volumes:
      - postgres-db-volume:/var/lib/postgresql/data
    
  mlflow-server:
    container_name: mlflow-server
    image: mlflow:test
    restart: unless-stopped
    depends_on:
      - "db"
    ports:
      - ${MLFLOW_PORT}:${MLFLOW_PORT}
    environment:
      - BACKEND=postgresql://${DB_USER}:${DB_PW}@db:${DB_PORT}/${DB_NAME}
    entrypoint:
      - "/bin/sh"
      - "-c"
      - "mlflow server --host 0.0.0.0 --port ${MLFLOW_PORT} --backend-store-uri $${BACKEND} --default-artifact-root file:${ML_MODEL_DIR}"
    healthcheck:
      test : ["CMD", "wget", "-O/dev/null", "-q", "http://localhost:${MLFLOW_PORT}/"]
      interval: 15s
      timeout: 15s
      retries: 3
    volumes:
      - mlflow-volume:/

volumes:
  postgres-db-volume:
    driver: local
    driver_opts:
      type: "none"
      o: "bind"
      device: "/data/postgresql"
  mlflow-volume:
    driver: local
    driver_opts:
      type: "none"
      o: "bind"
      device: "data/mlflow"
```
