# Use a lightweight Python image
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Copy all project files into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Expose FastAPI on port 5000
EXPOSE 5000

# Run FastAPI app on port 5000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
