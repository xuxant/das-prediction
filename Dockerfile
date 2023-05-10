FROM python:3.10.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENV PYTHONPATH="$PYTHONPATH:/app/src"

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0"]