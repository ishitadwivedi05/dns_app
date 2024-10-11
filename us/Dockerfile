# User Server Dockerfile
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the application code
COPY us.py .

# Install required packages
RUN pip install Flask requests

# Expose the port for the User Server
EXPOSE 8080

# Command to run the User Server
CMD ["python", "us.py"]
