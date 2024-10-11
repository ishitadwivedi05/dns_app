# Authoritative Server Dockerfile
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the application code
COPY as.py .

# Expose the port for the Authoritative Server
EXPOSE 53533/udp

# Command to run the Authoritative Server
CMD ["python", "as.py"]
