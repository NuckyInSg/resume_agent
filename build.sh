#!/bin/bash

# 停止并删除旧的容器（如果存在）
docker stop resume-converter-container 2>/dev/null
docker rm resume-converter-container 2>/dev/null

# 构建 Docker 镜像
echo "Building Docker image..."
docker build -t resume-converter .

# 运行新的容器
echo "Running Docker container..."
docker run -d --name resume-converter-container \
           -p 8000:8000 \
           -e ANTHROPIC_API_KEY="${ANTHROPIC_API_KEY}" \
           -e ANTHROPIC_API_URL="${ANTHROPIC_API_URL}" \
           resume-converter

# 显示容器日志
echo "Container logs:"
docker logs resume-converter-container

echo "Application is now running on http://localhost:8000"