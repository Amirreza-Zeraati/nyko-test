# Deployment Guide - ADHD Screening Expert System

## Quick Start

### Option 1: Docker (Recommended)

```bash
# Build and run with Docker Compose
docker-compose up -d

# Access application
open http://localhost:8000

# View logs
docker-compose logs -f

# Stop application
docker-compose down
```

### Option 2: Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Access at http://localhost:8000
```

## Production Deployment

### Using Docker on VPS

1. **Prepare VPS**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo apt install docker-compose -y
```

2. **Deploy Application**
```bash
# Clone repository
git clone https://github.com/Amirreza-Zeraati/nyko-test.git
cd nyko-test

# Configure environment
cp .env.example .env
nano .env  # Edit configuration

# Build and start
docker-compose up -d
```

3. **Setup Nginx Reverse Proxy**
```nginx
# /etc/nginx/sites-available/adhd-screening
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/adhd-screening /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Setup SSL with Let's Encrypt
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d yourdomain.com
```

### Environment Variables

Create `.env` file:

```env
# Application
ENV=production
DEBUG=False
SECRET_KEY=your-secret-key-here

# Server
HOST=0.0.0.0
PORT=8000

# CORS (if needed)
ALLOWED_ORIGINS=https://yourdomain.com

# Session
SESSION_TIMEOUT=3600

# Logging
LOG_LEVEL=INFO
```

## Monitoring

### Health Check
```bash
curl http://localhost:8000/health
```

### Logs
```bash
# Docker logs
docker-compose logs -f web

# Application logs (if file logging enabled)
tail -f logs/app.log
```

### Resource Usage
```bash
# Container stats
docker stats

# System resources
htop
```

## Backup

```bash
# Backup session data (if using persistent storage)
tar -czf backup-$(date +%Y%m%d).tar.gz data/

# Backup configuration
cp .env .env.backup
```

## Updates

```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose build
docker-compose up -d
```

## Security Considerations

1. **HTTPS**: Always use SSL/TLS in production
2. **Firewall**: Configure UFW or similar
```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```
3. **Rate Limiting**: Configure Nginx rate limiting
4. **Environment Variables**: Never commit `.env` to git
5. **Session Security**: Use secure session keys

## Troubleshooting

### Application Won't Start
```bash
# Check logs
docker-compose logs web

# Verify environment
docker-compose config

# Test locally
python -c "from app.main import app; print('OK')"
```

### Performance Issues
```bash
# Increase workers (in Dockerfile)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]

# Monitor resources
docker stats
```

### Database Connection Issues
- Verify database is running
- Check connection string
- Test connectivity: `telnet localhost 5432`

## Scaling

For high traffic:

1. **Horizontal Scaling**: Deploy multiple instances behind load balancer
2. **Caching**: Implement Redis for session storage
3. **Database**: Use PostgreSQL for persistence
4. **CDN**: Serve static files via CDN

## Support

For issues:
1. Check application logs
2. Review GitHub issues
3. Contact: [GitHub](https://github.com/Amirreza-Zeraati/nyko-test)
