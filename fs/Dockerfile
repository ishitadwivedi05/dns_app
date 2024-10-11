# Fibonacci Server Dockerfile
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the application code
COPY fs.py .

# Install required packages
RUN pip install Flask

# Expose the port for the Fibonacci Server
EXPOSE 9090

# Command to run the Fibonacci Server
CMD ["python", "fs.py"]
