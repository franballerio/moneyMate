# MoneyMate - Docker & Deployment Guide

Complete guide for running the entire MoneyMate stack with Docker Compose.

## Overview

The docker-compose.yml includes three services:
- **PostgreSQL 15**: Database service
- **FastAPI Backend**: Backend API server
- **React Frontend**: Frontend web application

## Quick Start

### 1. Clone & Navigate
```bash
cd /home/fballerio/projects/moneyMate
```

### 2. Create Environment File
```bash
cp .env.example .env
```

### 3. Start All Services
```bash
docker-compose up -d
```

### 4. Access Services
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Database**: localhost:5432

### 5. Stop Services
```bash
docker-compose down
```

---

## Service Details

### PostgreSQL Database
```yaml
- Port: 5432
- Username: user (default)
- Password: password (default)
- Database: moneymate
- Volume: postgres_data (persisted)
```

**Environment Variables:**
- `DB_USER`: PostgreSQL username
- `DB_PASSWORD`: PostgreSQL password
- `DB_NAME`: Database name
- `DB_PORT`: Port mapping

### FastAPI Backend
```yaml
- Port: 8000
- Host: http://backend:8000 (internal)
- Depends on: postgres (healthcheck)
- Volume: ./backend:/app (live reload)
```

**Environment Variables:**
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT secret key
- `JWT_EXPIRATION_HOURS`: Token expiration
- `CORS_ORIGINS`: Allowed frontend origins
- `LOG_LEVEL`: Logging level (INFO, DEBUG, etc.)
- `ENVIRONMENT`: Environment (development/production)

**API Endpoints:**
- `GET /health` - Health check
- `GET /api/v1/expenses` - List expenses
- `GET /api/v1/metrics/summary` - Spending summary
- `GET /api/v1/metrics/categories` - Category breakdown
- `GET /api/v1/metrics/trends` - Spending trends
- `GET /api/v1/budgets` - List budgets

### React Frontend
```yaml
- Port: 3000
- Host: http://localhost:3000
- Build: Multi-stage (Node 18-alpine)
- Depends on: backend
```

**Environment Variables:**
- `VITE_API_BASE_URL`: Backend API URL
- `VITE_ENVIRONMENT`: Environment (development/production)

---

## Configuration

### Environment Variables (.env file)

```bash
# Database
DB_USER=user
DB_PASSWORD=password
DB_NAME=moneymate
DB_PORT=5432

# Backend
SECRET_KEY=your-secret-key
JWT_EXPIRATION_HOURS=24
LOG_LEVEL=INFO
ENVIRONMENT=development
BACKEND_PORT=8000

# Frontend
FRONTEND_PORT=3000
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_ENVIRONMENT=development
```

### CORS Configuration
The backend is configured to accept requests from:
- `http://localhost:5173` - Development frontend
- `http://localhost:3000` - Production frontend
- `http://frontend:3000` - Docker compose frontend

Update `CORS_ORIGINS` in `.env` to add more origins:
```bash
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
```

---

## Docker Compose Commands

### Start Services
```bash
# Start all services in background
docker-compose up -d

# Start with verbose output
docker-compose up

# Start specific service
docker-compose up -d backend
```

### Stop Services
```bash
# Stop all services
docker-compose down

# Stop and remove volumes (careful - data loss!)
docker-compose down -v
```

### View Logs
```bash
# View all logs
docker-compose logs

# Follow logs from specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres

# View last 100 lines
docker-compose logs --tail=100
```

### Service Management
```bash
# Rebuild images
docker-compose build

# Rebuild and restart services
docker-compose up -d --build

# Restart specific service
docker-compose restart backend

# View running containers
docker-compose ps

# Execute command in container
docker-compose exec backend bash
docker-compose exec frontend sh
docker-compose exec postgres psql -U user -d moneymate
```

---

## Development Workflow

### Local Development (No Docker)

If you prefer local development without Docker:

```bash
# Terminal 1: Frontend
cd frontend
npm install
npm run dev
# Runs on http://localhost:5173

# Terminal 2: Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
# Runs on http://localhost:8000

# Terminal 3: Database
# Use local PostgreSQL or docker run postgres:15
docker run -e POSTGRES_PASSWORD=password -e POSTGRES_DB=moneymate -p 5432:5432 postgres:15
```

### Docker Development

```bash
# Build and start services
docker-compose up -d

# Backend code changes auto-reload (volume mounted)
# Frontend changes require rebuild:
docker-compose build frontend
docker-compose up -d frontend

# Check logs
docker-compose logs -f
```

---

## Production Deployment

### Pre-Production Checklist

1. **Environment Variables**
   ```bash
   # Update in .env for production
   ENVIRONMENT=production
   SECRET_KEY=<generate-secure-key>
   POSTGRES_PASSWORD=<strong-password>
   ```

2. **Database**
   ```bash
   # Run migrations
   docker-compose exec backend alembic upgrade head
   ```

3. **Security**
   - Change default passwords
   - Use strong SECRET_KEY
   - Set CORS_ORIGINS to production domain only
   - Enable HTTPS

### Production Docker Compose

```bash
# Use production override file
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### Build & Push Images

```bash
# Build images
docker-compose build

# Tag images
docker tag moneymate-frontend:latest your-registry/moneymate-frontend:latest
docker tag moneymate-backend:latest your-registry/moneymate-backend:latest

# Push to registry
docker push your-registry/moneymate-frontend:latest
docker push your-registry/moneymate-backend:latest
```

### Deploy to Production Server

```bash
# Pull latest images
docker pull your-registry/moneymate-frontend:latest
docker pull your-registry/moneymate-backend:latest

# Start services
docker-compose up -d

# Check health
docker-compose ps
docker-compose exec backend curl http://localhost:8000/health
```

---

## Troubleshooting

### Services Won't Start

```bash
# Check logs
docker-compose logs

# Check service status
docker-compose ps

# Rebuild everything
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### Backend Connection Issues

```bash
# Test backend health
docker-compose exec backend curl http://localhost:8000/health

# Check environment variables
docker-compose exec backend env | grep DATABASE_URL

# Check database connection
docker-compose exec backend python -c "from core.database import engine; print(engine)"
```

### Frontend Can't Reach Backend

```bash
# Check VITE_API_BASE_URL
docker-compose exec frontend env | grep VITE_API_BASE_URL

# Test backend from frontend container
docker-compose exec frontend wget http://backend:8000/health

# Check CORS configuration
# Browser console: Look for CORS error messages
```

### Database Issues

```bash
# Connect to database
docker-compose exec postgres psql -U user -d moneymate

# List tables
\dt

# Check migrations
\d alembic_version

# Exit psql
\q
```

### Port Already in Use

```bash
# Find process using port
lsof -i :3000  # Frontend
lsof -i :8000  # Backend
lsof -i :5432  # Database

# Kill process
kill -9 <PID>

# Or change ports in .env
FRONTEND_PORT=3001
BACKEND_PORT=8001
DB_PORT=5433
```

---

## Performance Tips

### Database
- Regular backups: `docker-compose exec postgres pg_dump -U user moneymate > backup.sql`
- Monitor connections: `docker-compose exec postgres psql -U user -c "SELECT datname, count(*) FROM pg_stat_activity GROUP BY datname;"`

### Backend
- Enable Uvicorn workers: `uvicorn main:app --workers 4`
- Use connection pooling for many concurrent requests
- Monitor logs for slow queries

### Frontend
- Bundle size: Check `dist/` after build
- Enable HTTP/2 at reverse proxy
- Use CDN for static assets

---

## Monitoring & Logging

### View All Logs
```bash
docker-compose logs -f
```

### Log to File
```bash
docker-compose logs > moneymate.log 2>&1 &
```

### Monitor Resource Usage
```bash
docker stats moneymate_backend moneymate_frontend moneymate_db
```

---

## Backup & Restore

### Backup Database

```bash
# Backup to SQL file
docker-compose exec -T postgres pg_dump -U user moneymate > backup_$(date +%Y%m%d).sql

# Backup to compressed file
docker-compose exec -T postgres pg_dump -U user moneymate | gzip > backup.sql.gz
```

### Restore Database

```bash
# From SQL file
docker-compose exec -T postgres psql -U user moneymate < backup.sql

# From compressed file
gunzip < backup.sql.gz | docker-compose exec -T postgres psql -U user moneymate
```

---

## Network Architecture

```
┌────────────────────────────────────────────┐
│        moneymate_network (bridge)          │
├────────────────────────────────────────────┤
│                                            │
│  ┌──────────────┐  ┌──────────────────┐   │
│  │   Frontend   │  │    Backend       │   │
│  │ :3000        │  │ :8000            │   │
│  │              │--│ http://backend   │   │
│  └──────────────┘  │ :8000            │   │
│        │           └────────┬─────────┘   │
│        │                    │             │
│        │          ┌─────────▼──────────┐  │
│        │          │   PostgreSQL       │  │
│        │          │ :5432              │  │
│        │          │ postgres:5432      │  │
│        └─────────▶│                    │  │
│                   └────────────────────┘  │
│                                            │
└────────────────────────────────────────────┘

External Access:
- Frontend: localhost:3000
- Backend: localhost:8000
- Database: localhost:5432
```

---

## File Structure

```
moneyMate/
├── docker-compose.yml       # Main compose file
├── .env                     # Environment variables
├── .env.example            # Example env file
├── backend/
│   ├── Dockerfile          # Backend image
│   ├── main.py            # FastAPI app
│   ├── requirements.txt    # Python dependencies
│   └── ...
├── frontend/
│   ├── Dockerfile         # Frontend image
│   ├── package.json       # Node dependencies
│   ├── vite.config.ts     # Vite config
│   └── ...
└── data/
    └── postgres/          # Database persistence
```

---

## Common Tasks

### Add New Environment Variable
1. Add to `.env` file
2. Add to appropriate service in `docker-compose.yml`
3. Rebuild: `docker-compose build`
4. Restart: `docker-compose up -d`

### Scale Backend Service
```yaml
# In docker-compose.yml, use docker swarm or multiple instances
# For development, typically not needed
```

### Enable Hot Reload
```yaml
# Backend: Already enabled with volume mount
# Frontend: Rebuild required
docker-compose build frontend
docker-compose up -d frontend
```

### Access Database from Host
```bash
# Using Docker CLI
docker-compose exec postgres psql -U user moneymate

# Or connect with your SQL client
# Host: localhost
# Port: 5432
# Username: user
# Password: password
# Database: moneymate
```

---

## Next Steps

1. **Start Services**: `docker-compose up -d`
2. **Check Status**: `docker-compose ps`
3. **View Logs**: `docker-compose logs -f`
4. **Access Frontend**: http://localhost:3000
5. **API Documentation**: http://localhost:8000/docs
6. **Database**: Connect with psql or DBeaver

## Support

- Frontend Issues: Check browser console and `docker-compose logs frontend`
- Backend Issues: Check `docker-compose logs backend`
- Database Issues: Check `docker-compose logs postgres`
- Network Issues: Verify service names and ports in docker-compose.yml

---

**Last Updated**: 2026-04-29
**Docker Compose Version**: 3.8
**Status**: ✅ Ready for Development & Production
