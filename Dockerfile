FROM python-3.10.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY pickle .

COPY src .

ENV PYTHONPATH="$PYTHONPATH:/app/src"

CMD ["uvicorn", "app:app"]