---
sidebar_position: 1
---

# Deployment Setup Guide

This guide provides step-by-step instructions for deploying CerebroMCP in a production environment.

## Prerequisites

Before deployment, ensure you have:

1. Python 3.8 or higher
2. Docker (optional, for containerized deployment)
3. A valid API key
4. Required system resources:
   - CPU: 2+ cores
   - RAM: 4GB minimum
   - Storage: 10GB minimum

## Installation

### 1. Package Installation

Install the CerebroMCP package:

```bash
pip install cerebromcp
```

### 2. Environment Setup

Set up your environment variables:

```bash
# Create a .env file
echo "MCP_API_KEY=your_api_key" > .env
echo "MCP_LOG_LEVEL=INFO" >> .env
echo "MCP_MAX_RETRIES=3" >> .env
```

## Configuration

### 1. Basic Configuration

Create a configuration file (`config.yaml`):

```yaml
# config.yaml
api:
  key: ${MCP_API_KEY}
  max_retries: 3
  timeout: 30

models:
  - name: gpt-4
    capabilities: ["text-generation", "code-completion"]
    max_tokens: 8192
  - name: gpt-3.5-turbo
    capabilities: ["text-generation"]
    max_tokens: 4096

logging:
  level: INFO
  file: /var/log/cerebromcp.log
```

### 2. Advanced Configuration

For production environments, add these settings:

```yaml
# config.yaml (production)
api:
  key: ${MCP_API_KEY}
  max_retries: 3
  timeout: 30
  rate_limit:
    requests_per_minute: 100
    burst_size: 10

models:
  - name: gpt-4
    capabilities: ["text-generation", "code-completion"]
    max_tokens: 8192
    priority: 1
  - name: gpt-3.5-turbo
    capabilities: ["text-generation"]
    max_tokens: 4096
    priority: 2

logging:
  level: INFO
  file: /var/log/cerebromcp.log
  rotation:
    max_size: 100MB
    backup_count: 5

monitoring:
  enabled: true
  metrics_port: 9090
  health_check:
    interval: 30s
    timeout: 5s
```

## Deployment Methods

### 1. Direct Deployment

Run the application directly:

```bash
python -m cerebromcp.server
```

### 2. Docker Deployment

Create a Dockerfile:

```dockerfile
FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV MCP_API_KEY=your_api_key
ENV MCP_LOG_LEVEL=INFO

CMD ["python", "-m", "cerebromcp.server"]
```

Build and run the container:

```bash
docker build -t cerebromcp .
docker run -d -p 8000:8000 cerebromcp
```

### 3. Kubernetes Deployment

Create a deployment configuration:

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cerebromcp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: cerebromcp
  template:
    metadata:
      labels:
        app: cerebromcp
    spec:
      containers:
      - name: cerebromcp
        image: cerebromcp:latest
        ports:
        - containerPort: 8000
        env:
        - name: MCP_API_KEY
          valueFrom:
            secretKeyRef:
              name: cerebromcp-secrets
              key: api-key
```

## Security Considerations

### 1. API Key Management

Store API keys securely:

```bash
# Using Kubernetes secrets
kubectl create secret generic cerebromcp-secrets \
  --from-literal=api-key=your_api_key
```

### 2. Network Security

Configure firewall rules:

```bash
# Allow only necessary ports
sudo ufw allow 8000/tcp  # API port
sudo ufw allow 9090/tcp  # Metrics port
```

### 3. SSL/TLS Configuration

Enable HTTPS:

```yaml
# config.yaml
api:
  ssl:
    enabled: true
    cert_file: /path/to/cert.pem
    key_file: /path/to/key.pem
```

## Monitoring Setup

### 1. Basic Monitoring

Enable basic monitoring:

```yaml
# config.yaml
monitoring:
  enabled: true
  metrics_port: 9090
  health_check:
    interval: 30s
    timeout: 5s
```

### 2. Advanced Monitoring

Set up Prometheus and Grafana:

```yaml
# prometheus-config.yaml
scrape_configs:
  - job_name: 'cerebromcp'
    static_configs:
      - targets: ['cerebromcp:9090']
```

## Troubleshooting

### Common Issues

1. **API Connection Issues**
   - Check API key validity
   - Verify network connectivity
   - Check rate limits

2. **Performance Issues**
   - Monitor resource usage
   - Check model availability
   - Review configuration

### Logging

Enable detailed logging:

```yaml
# config.yaml
logging:
  level: DEBUG
  file: /var/log/cerebromcp.log
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

## Next Steps

- Learn about [Scaling](../deployment/scaling)
- Set up [Monitoring](../deployment/monitoring)
- Review [Best Practices](../best-practices/model-selection) 