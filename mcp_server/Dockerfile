# Use Ubuntu base image and install both OpenJDK and Python 3.13
FROM eclipse-temurin:21.0.7_6-jre-alpine as base

# Set working directory
WORKDIR /app

# Install Python 3.13 and other dependencies (Java already included in base image)
RUN apk add --no-cache \
    git \
    build-base \
    curl \
    sed \
    python3 \
    py3-pip \
    bash \
    dos2unix

# Install PDM
RUN python3 -m pip install --break-system-packages pdm

# Copy project files
COPY pyproject.toml /app/
COPY README.md /app/
COPY mcp.json /app/
COPY bin/ /app/bin/
COPY src/ /app/src/
COPY entrypoint.sh /app/entrypoint.sh

# Fix line endings and make scripts executable
RUN dos2unix /app/entrypoint.sh /app/bin/*.sh && \
    chmod +x /app/bin/*.sh && chmod +x /app/entrypoint.sh

# Set environment variables
ENV PYTHONPATH=/app/src

# Expose port for Swagger UI
EXPOSE 8000

# Default command runs Swagger UI
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["swagger"]