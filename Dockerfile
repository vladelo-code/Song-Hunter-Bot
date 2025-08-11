FROM python:3.11-slim

LABEL authors="vladelo"

WORKDIR /app

COPY requirements.txt .

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH="${PYTHONPATH}:/app"

CMD alembic upgrade head && python app/bot.py

