# 🚀 PomPom-A2A Deployment Guide

This guide covers various deployment strategies for your PomPom-A2A agents, from development to production.

## 🎯 Deployment Options

### 🏠 Local Development
Perfect for testing and development.

### ☁️ Cloud Platforms
- **Heroku**: Simple deployment with git push
- **Railway**: Modern platform with automatic deployments
- **Render**: Easy container deployment
- **DigitalOcean App Platform**: Managed container platform
- **AWS**: Full-featured cloud deployment
- **Google Cloud**: Scalable cloud infrastructure
- **Azure**: Microsoft cloud platform

### 🐳 Container Platforms
- **Docker**: Containerized deployment
- **Kubernetes**: Orchestrated container deployment
- **Docker Swarm**: Simple container orchestration

### 🔧 Self-Hosted
- **VPS**: Virtual private servers
- **Dedicated Servers**: Full control deployment
- **On-Premises**: Internal infrastructure

## 🐳 Docker Deployment

### Basic Dockerfile
```dockerfile
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 agent && chown -R agent:agent /app
USER agent

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Multi-stage Dockerfile (Optimized)
```dockerfile
# Build stage
FROM python:3.12-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.12-slim

WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 agent && chown -R agent:agent /app
USER agent

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose
```yaml
version: '3.8'

services:
  agent:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/agents
      - REDIS_URL=redis://redis:6379
      - LOG_LEVEL=info
    depends_on:
      - db
      - redis
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: agents
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - agent
    restart: unless-stopped

volumes:
  postgres_data:
```

## ☁️ Cloud Platform Deployment

### Heroku
```bash
# Install Heroku CLI and login
heroku login

# Create app
heroku create my-pompom-agent

# Set environment variables
heroku config:set DATABASE_URL=your_database_url
heroku config:set API_KEY=your_api_key

# Deploy
git push heroku main

# Scale
heroku ps:scale web=1
```

**Procfile**:
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Railway
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

**railway.json**:
```json
{
  "build": {
    "builder": "DOCKERFILE"
  },
  "deploy": {
    "startCommand": "uvicorn main:app --host 0.0.0.0 --port $PORT",
    "healthcheckPath": "/health"
  }
}
```

### Render
**render.yaml**:
```yaml
services:
  - type: web
    name: pompom-agent
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    healthCheckPath: /health
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: pompom-db
          property: connectionString
      - key: PYTHON_VERSION
        value: 3.12.0

databases:
  - name: pompom-db
    databaseName: agents
    user: agent_user
```

### AWS (ECS with Fargate)
**task-definition.json**:
```json
{
  "family": "pompom-agent",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "pompom-agent",
      "image": "your-account.dkr.ecr.region.amazonaws.com/pompom-agent:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "DATABASE_URL",
          "value": "your-database-url"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/pompom-agent",
          "awslogs-region": "us-west-2",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

## 🎛️ Kubernetes Deployment

### Basic Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pompom-agent
  labels:
    app: pompom-agent
spec:
  replicas: 3
  selector:
    matchLabels:
      app: pompom-agent
  template:
    metadata:
      labels:
        app: pompom-agent
    spec:
      containers:
      - name: agent
        image: pompom-agent:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
        - name: LOG_LEVEL
          value: "info"
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: pompom-agent-service
spec:
  selector:
    app: pompom-agent
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

### Ingress Configuration
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: pompom-agent-ingress
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/rate-limit: "100"
spec:
  tls:
  - hosts:
    - api.pompom-agent.com
    secretName: pompom-agent-tls
  rules:
  - host: api.pompom-agent.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: pompom-agent-service
            port:
              number: 80
```

### ConfigMap and Secrets
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: pompom-agent-config
data:
  LOG_LEVEL: "info"
  MAX_WORKERS: "4"
  TIMEOUT: "30"
---
apiVersion: v1
kind: Secret
metadata:
  name: pompom-agent-secrets
type: Opaque
data:
  DATABASE_URL: <base64-encoded-url>
  API_KEY: <base64-encoded-key>
```

## 🔧 Production Configuration

### Environment Variables
```bash
# Application
APP_NAME=pompom-agent
APP_VERSION=1.0.0
LOG_LEVEL=info
DEBUG=false

# Server
HOST=0.0.0.0
PORT=8000
WORKERS=4
TIMEOUT=30

# Database
DATABASE_URL=postgresql://user:pass@host:5432/db
DATABASE_POOL_SIZE=10
DATABASE_MAX_OVERFLOW=20

# Redis (for caching/sessions)
REDIS_URL=redis://host:6379/0

# Security
SECRET_KEY=your-secret-key
API_KEY=your-api-key
CORS_ORIGINS=https://yourdomain.com

# Monitoring
SENTRY_DSN=your-sentry-dsn
PROMETHEUS_ENABLED=true
```

### Nginx Configuration
```nginx
upstream pompom_agent {
    server agent1:8000;
    server agent2:8000;
    server agent3:8000;
}

server {
    listen 80;
    server_name api.pompom-agent.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.pompom-agent.com;

    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;

    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req zone=api burst=20 nodelay;

    location / {
        proxy_pass http://pompom_agent;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    location /health {
        access_log off;
        proxy_pass http://pompom_agent;
    }
}
```

## 📊 Monitoring and Logging

### Health Check Endpoint
```python
from fastapi import FastAPI, HTTPException
import asyncio
import time

@app.get("/health")
async def health_check():
    """Health check endpoint for load balancers."""
    try:
        # Check database connection
        await check_database()
        
        # Check external dependencies
        await check_external_services()
        
        return {
            "status": "healthy",
            "timestamp": time.time(),
            "version": "1.0.0"
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service unhealthy: {str(e)}")

@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint."""
    # Return Prometheus-formatted metrics
    pass
```

### Logging Configuration
```python
import logging
import sys
from pythonjsonlogger import jsonlogger

def setup_logging():
    """Configure structured logging."""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    handler = logging.StreamHandler(sys.stdout)
    formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(name)s %(levelname)s %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger
```

## 🔒 Security Considerations

### HTTPS/TLS
- Always use HTTPS in production
- Use proper SSL certificates (Let's Encrypt)
- Configure strong cipher suites

### Authentication
```python
from fastapi import Depends, HTTPException, Header

async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != os.getenv("API_KEY"):
        raise HTTPException(401, "Invalid API key")
    return x_api_key

@app.post("/agent/message")
async def send_message(
    message: Message,
    api_key: str = Depends(verify_api_key)
):
    # Your agent logic
    pass
```

### Rate Limiting
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/agent/message")
@limiter.limit("10/minute")
async def send_message(request: Request, message: Message):
    # Your agent logic
    pass
```

## 🚀 Scaling Strategies

### Horizontal Scaling
- Multiple agent instances behind load balancer
- Stateless design for easy scaling
- Database connection pooling

### Vertical Scaling
- Increase CPU/memory resources
- Optimize database queries
- Use caching (Redis)

### Auto-scaling
```yaml
# Kubernetes HPA
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: pompom-agent-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: pompom-agent
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

## 🔍 Troubleshooting

### Common Issues
1. **Port conflicts**: Ensure port 8000 is available
2. **Database connections**: Check connection strings and firewall
3. **Memory issues**: Monitor memory usage and adjust limits
4. **SSL certificates**: Verify certificate validity and paths

### Debugging Commands
```bash
# Check container logs
docker logs pompom-agent

# Check Kubernetes pods
kubectl get pods
kubectl logs deployment/pompom-agent

# Check service status
kubectl get services
kubectl describe service pompom-agent-service

# Port forwarding for debugging
kubectl port-forward deployment/pompom-agent 8000:8000
```

---

*Deploy your PomPom-A2A agents with confidence! 🍮🚀*