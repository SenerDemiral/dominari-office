FROM python:3.11-slim

WORKDIR /app

# Gerekli kütüphaneleri yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 8000 portunda uvicorn'u başlat
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]