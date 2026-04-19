FROM python:3.11-slim

WORKDIR /app

# Install dependencies (cache layer)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Environment
ENV PYTHONPATH=/app/src
ENV PYTHONUNBUFFERED=1

# Copy app
COPY src/ ./src/

# Data directory (SQLite)
RUN mkdir -p data
VOLUME ["/app/data"]

EXPOSE 8501

CMD ["streamlit", "run", "src/app.py", "--server.address=0.0.0.0", "--server.port=8501"]
