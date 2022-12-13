# Mlflow
MLflow는 머신러닝(Machine learning) 모델의 실험을 tracking하고 model을 공유 및 deploy 할 수 있도록 지원하는 라이브러리

# mlflow dockerfile
``` docker
# 베이스 이미지
FROM continuumio/miniconda3:latest
WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y git
RUN pip install mlflow psycopg2-binary pymysql boto3

RUN cd /app && git clone https://github.com/mlflow/mlflow-example.git

COPY wait-for-it.sh wait-for-it.sh

RUN chmod +x wait-for-it.sh
```

# docker-compose 및 dockerfile
https://velog.io/@h13m0n/MLOps-MLFlow-with-Docker 참고하여 작성

``` yaml
version: "3.3"
services:
  db:
    container_name: mlflow-db
    # postgres 이미지
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
    # volume을 호스트 볼륨으로 설정(k8s 환경에서는 X), 볼륨설정을 안하면 이미지 삭제하면 저장되었던 데이터도 함꺠 삭제됨
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
      # --backend-store-uri : db위치 
      # --default-artifact-root : artifact가 저장될 위치
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