# Python ka official lightweight image lo
FROM python:3.10-slim

# Working directory set karo container ke andar
WORKDIR /app

# Requirements file copy karo aur dependencies install karo
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Baaki ka poora backend code copy karo
COPY . .

# FastAPI server run karne ke liye port expose karo
EXPOSE 8000

# Server start command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]