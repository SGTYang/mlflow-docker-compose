FROM continuumio/miniconda3:latest
WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y git
RUN pip install mlflow psycopg2-binary pymysql boto3

RUN cd /app && git clone https://github.com/mlflow/mlflow-example.git

COPY wait-for-it.sh wait-for-it.sh
RUN chmod +x wait-for-it.sh