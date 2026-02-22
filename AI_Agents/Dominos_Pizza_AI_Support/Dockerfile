# Use official Python slim image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Create necessary directories
RUN mkdir -p /app/hf_cache /app/Pizza_AI_Agent_DB && \
    chmod -R 777 /app/hf_cache /app/Pizza_AI_Agent_DB

# Set Hugging Face cache environment variable
ENV HF_HOME=/app/hf_cache
# Hugging Face API Token should be passed as a secret or environment variable
# Example: docker run -e HUGGINGFACEHUB_API_TOKEN=<your_token> ...
# ENV HUGGINGFACEHUB_API_TOKEN=your_token_here

# Expose Flask port
EXPOSE 7860

# Run Gunicorn with threaded workers
CMD ["gunicorn", "-b", "0.0.0.0:7860", "app:app", "-k", "gthread", "--threads", "2"]