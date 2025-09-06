# LogPie 🥧

A modern, structured logging system with data masking capabilities built with Python and FastAPI.

## 🎯 Overview

LogPie is a production-ready logging solution designed to handle sensitive data with built-in masking capabilities, structured logging, and real-time observability. Perfect for applications that need to log user interactions while maintaining privacy and compliance standards.

## ✨ Features

- **Structured Logging**: JSON-formatted logs with consistent schema
- **Data Masking**: Automatic detection and masking of sensitive information (emails, phones, CPF, etc.)
- **Request Context**: Automatic request ID generation and context injection
- **FastAPI Integration**: Built-in middleware for seamless API logging
- **Configurable Masking Rules**: YAML-based configuration for custom masking patterns
- **Production Ready**: Docker containerized with multi-stage builds

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Docker and Docker Compose
- uv (Python package manager)

### Local Development

1. Clone the repository:

```bash
git clone <repository-url>
cd logpie
```

2. Install dependencies:

```bash
uv sync
```

3. Run the application:

```bash
uv run uvicorn logpie.main:app --reload
```

The API will be available at `http://localhost:8000`.

## 🐳 Running with Docker Compose

This project runs in Docker Compose. Depending on your environment (Linux or macOS), there are differences in how logs are mounted in the container.

### 🐧 If you're running on **Linux**

Use **bind mount** to access log files directly from the host:

Create a `docker-compose.yml` file:

```yaml
# docker-compose.yml (Linux)
version: "3.9"
services:
  app:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./logs:/app/logs:delegated
    environment:
      - LOG_LEVEL=DEBUG
```

Run the application:

```bash
docker compose up --build
```

Log files will appear in the `./logs` folder in your project.

### 🍎 If you're running on **macOS (Docker Desktop or Colima)**

On macOS, bind mounts can cause permission errors or slowness.  
👉 In these cases, prefer a **named volume**:

Create a `docker-compose.yml` file:

```yaml
# docker-compose.yml (macOS)
version: "3.9"
services:
  app:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - logpie_logs:/app/logs
    environment:
      - LOG_LEVEL=DEBUG

volumes:
  logpie_logs:
```

Run the application:

```bash
docker compose up --build
```

To view logs:

```bash
# Inspect logs inside the container
docker compose run --rm app cat /app/logs/2025-09-06.log

# Copy logs from container to host
docker compose cp app:/app/logs ./local_logs_backup
```

### ✨ Environment Comparison

| Environment | Mount Type   | Log Access                     | Performance |
| ----------- | ------------ | ------------------------------ | ----------- |
| **Linux**   | Bind Mount   | Direct file access in `./logs` | ⚡ Fast     |
| **macOS**   | Named Volume | Via Docker commands            | 🐌 Stable   |

## 📋 API Endpoints

### Health Check

```bash
GET /
```

Returns application status and generates a sample log entry with masking demonstration.

## 🔧 Configuration

### Masking Rules

LogPie uses a YAML configuration file (`masking.yaml`) to define data masking patterns:

```yaml
masking_rules:
  email:
    pattern: "\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    replacement: "***@***.***"

  phone:
    pattern: "\b\d{2}\s?\d{4,5}-?\d{4}\b"
    replacement: "(**) ****-****"

  cpf:
    pattern: "\b\d{3}\.\d{3}\.\d{3}-\d{2}\b"
    replacement: "***.***.**-**"
```

### Environment Variables

- `LOG_LEVEL`: Set logging level (DEBUG, INFO, WARNING, ERROR)

## 🏗️ Architecture

LogPie follows a modular architecture:

```
logpie/
├── core/
│   ├── logger.py          # Core logging functionality
│   └── masking_engine.py  # Data masking implementation
├── config/
│   ├── masking_config.py  # Configuration loader
│   └── masking.yaml       # Masking rules definition
├── middleware/
│   └── logging_middleware.py  # FastAPI middleware
└── main.py               # FastAPI application
```

## 🧪 Testing

Run tests with:

```bash
uv run pytest
```

## 🚀 Production Deployment

The application is containerized using multi-stage Docker builds for optimal security and performance:

- **Builder stage**: Uses `python:3.11-slim` with build tools
- **Runtime stage**: Minimal runtime environment
- **Security**: Non-root user execution
- **Performance**: Optimized layer caching

## 🔒 Security Features

- **Data Masking**: Automatic PII detection and masking
- **Structured Logging**: Consistent log format for security monitoring
- **Request Tracing**: Unique request IDs for audit trails
- **Configurable Rules**: Flexible masking patterns for different data types

## 📈 Monitoring & Observability

LogPie generates structured JSON logs that integrate seamlessly with:

- **ELK Stack** (Elasticsearch, Logstash, Kibana)
- **Grafana + Loki**
- **Datadog**
- **New Relic**
- Any JSON-compatible log aggregation system

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🎯 Why LogPie?

LogPie was built to solve real-world problems in production environments:

- **Compliance**: Automatic PII masking for GDPR/LGPD compliance
- **Observability**: Structured logs for better monitoring and debugging
- **Performance**: Efficient masking engine with pre-compiled regex patterns
- **Scalability**: Designed for high-throughput applications
- **Developer Experience**: Simple integration with existing FastAPI applications

Perfect for demonstrating senior-level Python development skills with focus on:

- Clean architecture
- Security best practices
- Production readiness
- Docker containerization
- Structured logging
- Data privacy compliance
