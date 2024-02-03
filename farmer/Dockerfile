# https://hub.docker.com/_/python
FROM python:3.11-slim

ENV PYTHONUNBUFFERED True

ENV APP_HOME /app
WORKDIR $APP_HOME

RUN pip install --no-cache-dir fastapi uvicorn[standard]

COPY pyproject.toml .
COPY src src
RUN pip install --no-cache-dir .

ENV PORT 8080
CMD uvicorn farmer:app --host 0 --port $PORT
