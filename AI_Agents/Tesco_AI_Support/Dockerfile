# Stage 1: Build Frontend
FROM node:18-alpine as frontend-build
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build

# Stage 2: Setup Backend & Serve
FROM python:3.11-slim

WORKDIR /app

# Copy Backend Requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Backend Code
COPY . .

# Copy Frontend Build from Stage 1
COPY --from=frontend-build /app/frontend/dist /app/frontend/dist

# Expose Port 7860 (Hugging Face Default)
EXPOSE 7860

# Run Application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
