FROM python:3.9-slim

WORKDIR /app

COPY SelectNewsService.py .
COPY SelectNews.py .
COPY requirements.txt .

RUN apt-get update \
    && pip install --upgrade pip \
    && pip install Werkzeug==2.3.6 \
    && pip install --no-cache-dir gunicorn \
    && pip install --no-cache-dir -r requirements.txt

ENV PORT=8003

CMD ["gunicorn", "-b", "0.0.0.0:8003", "SelectNewsService:app"]