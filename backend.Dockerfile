FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY recommender/ /app/recommender/
COPY products/ /app/products/

ENV PYTHONPATH=/app
ENV PRODUCTS_DIR=/app/products

EXPOSE 8000

CMD ["uvicorn", "recommender.main:app", "--host", "0.0.0.0", "--port", "8000"]
