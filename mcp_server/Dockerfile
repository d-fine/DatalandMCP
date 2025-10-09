# Use Ubuntu base image and install both OpenJDK and Python 3.13
FROM eclipse-temurin:21.0.7_6-jre-alpine AS base

# Set working directory
WORKDIR /app

# Install Python 3.13 and other dependencies (Java already included in base image)
RUN apk add --no-cache \
    bash \
    build-base \
    curl \
    dos2unix \
    git \
    py3-pip \
    python3 \
    sed

# Install PDM
RUN python3 -m pip install --break-system-packages pdm

# Copy project files
COPY pyproject.toml /app/
COPY README.md /app/
COPY mcp.json /app/
COPY bin/ /app/bin/
COPY src/ /app/src/
COPY entrypoint.sh /app/entrypoint.sh
COPY healthcheck.sh /app/healthcheck.sh

# Fix line endings and make scripts executable
RUN dos2unix /app/entrypoint.sh /app/healthcheck.sh /app/bin/*.sh && \
    chmod +x /app/bin/*.sh && chmod +x /app/healthcheck.sh && chmod +x /app/entrypoint.sh

# Set environment variables
ENV PYTHONPATH=/app/src

# Expose ports for the servers
EXPOSE 8000
EXPOSE 8001

# Install dependencies and run mcp server
ENTRYPOINT ["/app/entrypoint.sh"]