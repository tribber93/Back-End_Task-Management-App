FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt --no-cache-dir

EXPOSE 8000

CMD python main.py