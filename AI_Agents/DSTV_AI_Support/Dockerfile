# Build stage for React frontend
FROM node:20-slim as build-frontend

WORKDIR /app/frontend
COPY frontend/package*.json ./
# Use --legacy-peer-deps to handle conflicts between React 19 and lucide-react
RUN npm ci --legacy-peer-deps || npm install --legacy-peer-deps
COPY frontend/ ./
# Run build, ensuring we see errors if they occur
RUN npm run build

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
# Combine into one layer and cleanup to keep image small
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY . .

# Copy built frontend from stage 1
COPY --from=build-frontend /app/frontend/dist ./frontend/dist

# Expose port
EXPOSE 7860

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860", "--loop", "asyncio"]