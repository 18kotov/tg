
FROM python:3.10-alpine

WORKDIR /app/

ADD . .

RUN pip install --upgrade pip && \
    pip install -U telethon && \
    pip install psycopg2-binary


CMD ["./parsing_posting.py"]
ENTRYPOINT ["python3"]
