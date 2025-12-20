FROM python:3.9-slim


WORKDIR /app


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . .


RUN mkdir -p /app/model_cache


RUN python preload_model.py


ENV SENTENCE_TRANSFORMERS_HOME=/app/model_cache
ENV FASTEMBED_CACHE_PATH=/app/model_cache
ENV HOME=/tmp

EXPOSE 10000


CMD ["sh", "-c", "chmod -R 777 /app/model_cache && uvicorn api:app --host 0.0.0.0 --port $PORT"]