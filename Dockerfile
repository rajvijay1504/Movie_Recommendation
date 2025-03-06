# Base image.
FROM python:3.8-slim

# Set working directory.
WORKDIR /app

# Copy dependencies.
COPY requirements.txt .

# Install dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files.
COPY . .

# Expose port.
EXPOSE 8080

# Run the app.
CMD ["python", "main.py"]
