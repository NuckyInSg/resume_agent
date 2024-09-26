#!/bin/bash

docker stop resume-converter-container 2>/dev/null
docker rm resume-converter-container 2>/dev/null

echo "Building Docker image..."
docker build -t resume-converter .

echo "Running Docker container..."
docker run -d --name resume-converter-container \
           -p 8000:8000 \
           -e ANTHROPIC_API_KEY="${ANTHROPIC_API_KEY}" \
           -e ANTHROPIC_API_URL="${ANTHROPIC_API_URL}" \
           resume-converter

echo "Container logs:"
docker logs resume-converter-container

echo "Application is now running on http://localhost:8000"
