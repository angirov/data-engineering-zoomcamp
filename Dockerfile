FROM python:3.10

WORKDIR /app
COPY "./requirements.txt" .
RUN pip install -r requirements.txt

COPY "./ingest_data.py" .
ENTRYPOINT [ "python3", "/app/ingest_data.py" ]
