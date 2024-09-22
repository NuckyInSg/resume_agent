# Use Debian Stable Slim as the base image
FROM debian:stable-slim

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Update package lists and install system dependencies
RUN echo "deb http://deb.debian.org/debian stable main" > /etc/apt/sources.list && \
    echo "deb http://deb.debian.org/debian stable-updates main" >> /etc/apt/sources.list && \
    echo "deb http://deb.debian.org/debian-security stable-security main" >> /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -qyf \
    curl jq make git \
    python3-pygments gnuplot \
    texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended \
    python3 python3-pip python3-venv && \
    rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . /app

# Create and activate virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run main.py when the container launches
CMD ["python3", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
