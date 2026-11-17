FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend ./backend
COPY data_engine ./data_engine
COPY sample_data ./sample_data
RUN mkdir -p /app/data/bronze /app/data/silver /app/data/gold
ENV PYTHONPATH=/app
EXPOSE 8000
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
