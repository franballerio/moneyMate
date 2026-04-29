# MoneyMate - Complete Setup & Integration Guide

This guide walks you through the complete setup, integration, and deployment of the MoneyMate full-stack application.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Quick Start (Docker)](#quick-start-docker)
3. [Local Development Setup](#local-development-setup)
4. [Frontend-Backend Integration](#frontend-backend-integration)
5. [Testing the Integration](#testing-the-integration)
6. [Troubleshooting](#troubleshooting)
7. [Deployment](#deployment)

---

## Prerequisites

### Required
- **Docker** and **Docker Compose** (recommended for full stack)
- **Node.js 16+** (for frontend development)
- **Python 3.9+** (for backend development)
- **PostgreSQL 15** (or use Docker)
- **Git** (for version control)

### Optional
- **PostgreSQL Client** (psql) - for database management
- **Postman or Insomnia** - for API testing
- **VS Code** with extensions - for development

---

## Quick Start (Docker)

The fastest way to get the entire stack running!

### Step 1: Clone Repository
```bash
cd /home/fballerio/projects/moneyMate
git clone <repo-url>  # If not already cloned
cd moneyMate
```

### Step 2: Setup Environment
```bash
# Copy example environment file
cp .env.example .env

# Edit .env if needed (defaults work for local development)
# nano .env
```

### Step 3: Start Services
```bash
# Start all services in background
docker-compose up -d

# Or start with logs visible
docker-compose up

# Wait 30-60 seconds for services to initialize
```

### Step 4: Verify Services
```bash
# Check service status
docker-compose ps

# Expected output:
# NAME                COMMAND                  SERVICE      STATUS
# moneymate_db        postgres                 postgres     Up (healthy)
# moneymate_backend   uvicorn main:app ...    backend      Up
# moneymate_frontend  serve -s dist -l 3000   frontend     Up
```

### Step 5: Access Services
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Database**: localhost:5432

### Step 6: View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
```

---

## Local Development Setup

For development without Docker (useful for debugging):

### Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Run database migrations
alembic upgrade head

# Start backend
python main.py
# Backend runs on http://localhost:8000
```

### Setup Frontend

```bash
cd frontend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env.local

# Start dev server
npm run dev
# Frontend runs on http://localhost:5173
```

### Setup Database (Option A: Docker)

```bash
# Run PostgreSQL in Docker
docker run -d \
  --name moneymate_postgres \
  -e POSTGRES_USER=user \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=moneymate \
  -p 5432:5432 \
  postgres:15

# Verify connection
docker exec moneymate_postgres psql -U user -d moneymate -c "SELECT 1;"
```

### Setup Database (Option B: Local PostgreSQL)

```bash
# Create database
createdb moneymate

# Run migrations
cd backend
alembic upgrade head

# Verify
psql -d moneymate -c "\dt"
```

---

## Frontend-Backend Integration

### API Configuration

The frontend connects to the backend through environment variables.

#### For Docker
```bash
# In .env (root directory)
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

#### For Local Development
```bash
# In frontend/.env.local
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

#### For Production
```bash
# In .env (root directory)
VITE_API_BASE_URL=https://your-domain.com/api/v1
```

### CORS Configuration

The backend allows requests from:
- Development: `http://localhost:5173` (Vite dev server)
- Docker: `http://localhost:3000` (frontend service)
- Custom: Edit `CORS_ORIGINS` in `.env`

### Service Discovery

#### Docker Network
Services communicate via internal network:
- Frontend → Backend: `http://backend:8000`
- Backend → Database: `postgresql://user:password@postgres:5432/moneymate`

#### Local Development
Services communicate via localhost:
- Frontend → Backend: `http://localhost:8000`
- Backend → Database: `postgresql://user:password@localhost:5432/moneymate`

---

## Testing the Integration

### 1. Test Backend Health

```bash
# Using curl
curl http://localhost:8000/health

# Expected response:
# {"status":"healthy"}
```

### 2. Test API Endpoints

```bash
# Get expenses
curl http://localhost:8000/api/v1/expenses

# Get metrics summary
curl http://localhost:8000/api/v1/metrics/summary

# Get API documentation
# Open in browser: http://localhost:8000/docs
```

### 3. Test Frontend-Backend Connection

```bash
# Check browser console (F12) for:
# - Network tab: Verify API calls to backend
# - Console tab: Check for CORS errors
# - Check that metrics load from backend
```

### 4. Test Database Connection

```bash
# From backend container
docker-compose exec backend python -c \
  "from core.database import engine; print(engine.url); engine.connect()"

# Or using psql
docker-compose exec postgres psql -U user -d moneymate -c "SELECT COUNT(*) FROM expenses;"
```

---

## Troubleshooting

### Services Won't Start

```bash
# Check error messages
docker-compose logs

# Rebuild everything
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d

# Check individual services
docker-compose ps
```

### Backend Connection Refused

```bash
# Check if backend is running
curl http://localhost:8000/health

# Check logs
docker-compose logs backend

# Verify DATABASE_URL
docker-compose exec backend env | grep DATABASE_URL

# Check PostgreSQL status
docker-compose ps postgres
```

### Frontend Can't Reach Backend

```bash
# Check VITE_API_BASE_URL in browser console
# Open DevTools → Application → Environment Variables

# Test from frontend container
docker-compose exec frontend wget http://backend:8000/health

# Check CORS errors in browser console
# If CORS error, update CORS_ORIGINS in .env
```

### Database Connection Failed

```bash
# Check PostgreSQL service
docker-compose ps postgres

# Test database directly
docker-compose exec postgres psql -U user -d moneymate -c "SELECT 1;"

# Check logs
docker-compose logs postgres

# Verify connection string
echo $DATABASE_URL
```

### Port Already in Use

```bash
# Find process using port
lsof -i :3000  # Frontend
lsof -i :8000  # Backend
lsof -i :5432  # Database

# Kill process
kill -9 <PID>

# Or use different ports in .env
FRONTEND_PORT=3001
BACKEND_PORT=8001
DB_PORT=5433
```

### API Returns 404

```bash
# Verify backend has correct routes
docker-compose exec backend python -c \
  "from main import app; [print(r.path) for r in app.routes]"

# Check API prefix matches frontend URL
# Backend: /api/v1/expenses
# Frontend should call: http://localhost:8000/api/v1/expenses
```

---

## Deployment

### Pre-Deployment Checklist

- [ ] Update `.env` with production values
- [ ] Change `SECRET_KEY` to secure random string
- [ ] Set `ENVIRONMENT=production`
- [ ] Update `VITE_API_BASE_URL` to production domain
- [ ] Update `CORS_ORIGINS` to production domain only
- [ ] Backup existing database
- [ ] Run database migrations: `alembic upgrade head`
- [ ] Test all API endpoints
- [ ] Build frontend: `npm run build`
- [ ] Test Docker build locally

### Deploy to Production

```bash
# 1. Pull latest code
git pull origin main

# 2. Update environment
cp .env.example .env
# Edit .env with production values

# 3. Build images
docker-compose build

# 4. Start services with production overrides
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# 5. Verify services
docker-compose ps
curl https://your-domain.com/health

# 6. Monitor logs
docker-compose logs -f
```

### Backup & Recovery

```bash
# Backup database
docker-compose exec -T postgres pg_dump -U user moneymate > backup_$(date +%Y%m%d).sql

# Backup .env
cp .env .env.backup

# Restore database (if needed)
docker-compose exec -T postgres psql -U user moneymate < backup_20240101.sql
```

### Monitoring

```bash
# View resource usage
docker stats

# Check service health
curl http://localhost:8000/health
curl http://localhost:3000/

# Monitor logs
docker-compose logs --tail=100 -f

# Backup regularly
0 2 * * * docker-compose exec -T postgres pg_dump -U user moneymate > /backups/backup_$(date +\%Y\%m\%d).sql
```

---

## Project Structure

```
moneyMate/
├── docker-compose.yml         # Main compose file
├── docker-compose.prod.yml    # Production overrides
├── .env                       # Environment variables
├── .env.example              # Example env file
│
├── backend/                   # FastAPI backend
│   ├── Dockerfile            # Backend image
│   ├── main.py              # FastAPI app
│   ├── api/v1/              # API routes
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   ├── services/            # Business logic
│   ├── core/                # Config & database
│   ├── repositories/        # Data access
│   ├── requirements.txt     # Python dependencies
│   └── alembic/            # Database migrations
│
├── frontend/                  # React frontend
│   ├── Dockerfile           # Frontend image
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API & hooks
│   │   └── App.tsx         # Main app
│   ├── package.json        # Node dependencies
│   ├── vite.config.ts      # Vite config
│   ├── tailwind.config.js  # TailwindCSS config
│   └── .env.local          # Local env
│
├── src/bot/                  # Telegram bot
│   ├── main.py             # Bot entry
│   ├── bot_logic/          # Bot logic
│   ├── services/           # Bot services
│   ├── handlers.py         # Message handlers
│   └── .env               # Bot env
│
├── PLAN.md                   # Implementation plan
├── FRONTEND_SUMMARY.md      # Frontend docs
├── STARTUP_GUIDE.md         # Startup guide
├── DOCKER_DEPLOYMENT.md     # Docker guide
└── SETUP_INTEGRATION.md     # This file
```

---

## Quick Commands Reference

```bash
# Docker Compose
docker-compose up -d              # Start all services
docker-compose down               # Stop services
docker-compose logs -f            # View logs
docker-compose ps                 # List services
docker-compose build              # Build images
docker-compose restart            # Restart services

# Frontend
npm install                       # Install dependencies
npm run dev                      # Start dev server
npm run build                    # Build for production
npm run preview                  # Preview production build

# Backend
python -m venv venv              # Create virtual env
source venv/bin/activate         # Activate (Linux/Mac)
pip install -r requirements.txt  # Install dependencies
alembic upgrade head             # Run migrations
python main.py                   # Start server

# Database
docker-compose exec postgres psql -U user -d moneymate  # Connect to DB
docker-compose exec -T postgres pg_dump -U user moneymate > backup.sql  # Backup

# Telegram Bot
python src/bot/main.py           # Start bot
```

---

## Support & Help

### Documentation
- Full Plan: `PLAN.md`
- Frontend: `frontend/README.md`
- Backend: `backend/README.md` (if exists)
- Docker: `DOCKER_DEPLOYMENT.md`
- This guide: `SETUP_INTEGRATION.md`

### Common Issues
1. **Services won't start**: Check `docker-compose logs`
2. **Frontend can't reach backend**: Verify `VITE_API_BASE_URL` and CORS
3. **Database errors**: Ensure PostgreSQL is running and migrations applied
4. **Port conflicts**: Change ports in `.env` and docker-compose.yml

### Getting Help
- Check logs: `docker-compose logs -f`
- Test endpoints: `curl http://localhost:8000/docs`
- Review environment: `docker-compose exec backend env`

---

## Next Steps

1. **Start Services**: `docker-compose up -d`
2. **Access Frontend**: http://localhost:3000
3. **Explore API**: http://localhost:8000/docs
4. **Monitor Logs**: `docker-compose logs -f`
5. **Test Endpoints**: Use Postman or curl

## Conclusion

You now have a fully integrated, containerized MoneyMate application ready for development or deployment. The frontend and backend communicate seamlessly through Docker's internal network or localhost, with PostgreSQL as the persistent data store.

For more information, refer to the relevant documentation files or the main PLAN.md.

---

**Last Updated**: 2026-04-29  
**Status**: ✅ Complete - Frontend & Backend Integrated & Containerized  
**Version**: 1.0
