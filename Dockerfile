FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

RUN mkdir -p /app/model_cache

RUN python preload_model.py

RUN chmod -R 777 /app/model_cache

RUN chmod 777 /app

ENV SENTENCE_TRANSFORMERS_HOME=/app/model_cache

EXPOSE 10000

CMD ["sh", "-c", "uvicorn api:app --host 0.0.0.0 --port $PORT"]