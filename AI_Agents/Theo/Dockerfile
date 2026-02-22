# ==============================================================
# Tech Disciples AI — Dockerfile (Minimalist Python Version)
# ==============================================================

FROM python:3.10-slim

# Environment setup
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_HOME=/app

WORKDIR $APP_HOME

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all source files (main.py, static/, templates/)
COPY . .

# Define Hugging Face token env var
ENV HUGGINGFACEHUB_API_TOKEN=""

# Expose port for FastAPI
EXPOSE 7860

# Launch the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
