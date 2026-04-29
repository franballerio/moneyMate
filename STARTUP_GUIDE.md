# MoneyMate - Full-Stack Development Guide

This guide walks you through setting up and running the complete MoneyMate stack locally.

## Project Structure

```
moneyMate/
├── bot/                    # Telegram Bot (Python)
├── backend/               # FastAPI Backend (Python) - TODO
├── frontend/              # React Frontend (TypeScript)
├── PLAN.md               # Full implementation plan
├── FRONTEND_SUMMARY.md   # Frontend documentation
├── requirements.txt      # Shared Python dependencies
└── docker-compose.yml    # Docker services - TODO
```

## Prerequisites

- **Node.js** 16+ (for frontend)
- **Python** 3.9+ (for bot and backend)
- **PostgreSQL** 15+ (or use Docker)
- **npm** or **yarn** (Node package manager)
- **pip** (Python package manager)

## Setup Instructions

### 1. Clone & Setup Project

```bash
cd /home/fballerio/projects/moneyMate
git clone <repo-url>  # If not already cloned
```

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env.local

# Edit .env.local if backend is on different URL
# VITE_API_BASE_URL=http://localhost:8000/api/v1

# Start dev server (runs on http://localhost:5173)
npm run dev
```

### 3. Backend Setup (TODO - Phase 2)

```bash
# Create Python virtual environment
python -m venv backend/venv

# Activate virtual environment
source backend/venv/bin/activate  # Linux/Mac
# or
backend\venv\Scripts\activate     # Windows

# Install dependencies (when available)
pip install -r backend/requirements.txt

# Run migrations (when available)
alembic upgrade head

# Start FastAPI server (runs on http://localhost:8000)
uvicorn main:app --reload
```

### 4. Telegram Bot Setup

```bash
cd src/bot

# Create Python virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r ../../requirements.txt

# Update .env file with:
# - TELEGRAM_TOKEN (get from BotFather)
# - DB_NAME (database name)
# - DATABASE_URL (when using PostgreSQL)

# Start the bot
python main.py
```

### 5. PostgreSQL Setup (Optional - currently using SQLite)

```bash
# Option A: Using Docker Compose (when available)
docker-compose up -d postgres

# Option B: Local PostgreSQL installation
# Create database
createdb moneymate

# Connect to database
psql moneymate
```

## Running the Full Stack

### Terminal 1: Frontend
```bash
cd frontend
npm run dev
# Access at http://localhost:5173
```

### Terminal 2: Backend (when available)
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload
# Access at http://localhost:8000
# Docs at http://localhost:8000/docs
```

### Terminal 3: Telegram Bot
```bash
cd src/bot
source venv/bin/activate
python main.py
```

## Environment Variables

### Frontend (.env.local)
```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_ENVIRONMENT=development
```

### Backend (.env - TODO)
```env
DATABASE_URL=postgresql://user:password@localhost:5432/moneymate
SECRET_KEY=your-secret-key-here
JWT_EXPIRATION_HOURS=24
CORS_ORIGINS=http://localhost:5173
LOG_LEVEL=INFO
```

### Bot (.env)
```env
TELEGRAM_TOKEN=your-bot-token-here
DB_NAME=spents
DATABASE_URL=postgresql://user:password@localhost:5432/moneymate
```

## Available Commands

### Frontend
```bash
npm run dev       # Start development server
npm run build     # Create production build
npm run preview   # Preview production build
```

### Backend (when available)
```bash
pytest            # Run tests
alembic revision  # Create migration
alembic upgrade   # Apply migrations
```

### Bot
```bash
python main.py    # Start bot
pytest tests/     # Run tests (when available)
```

## Frontend Features

### Dashboard
- Real-time spending metrics (daily, monthly, all-time)
- Spending trends visualization (line chart)
- Category breakdown (pie chart)
- Budget status and alerts

### Transactions
- Paginated transaction list (20 items per page)
- Filter by category
- Sort by date or amount
- View transaction details

### Navigation
- Sidebar with 5 main sections
- Header with user menu and notifications
- Responsive layout (desktop-first)

## Testing Frontend Locally

### Without Backend
1. Mock API responses in `src/services/api.ts`
2. Update hooks to return dummy data
3. Frontend will display placeholder data

### With Backend
1. Ensure backend is running on http://localhost:8000
2. Update `VITE_API_BASE_URL` in `.env.local`
3. Frontend will fetch real data from API

## Building for Production

### Frontend
```bash
cd frontend
npm run build

# Output: dist/ directory
# Upload to web server or CDN
```

### Backend (when available)
```bash
cd backend
# Setup environment variables
# Run migrations
# Start with production server (gunicorn/uvicorn)
```

### Bot
```bash
# Deploy to server with Python 3.9+
# Setup systemd service or supervisor
# Configure environment variables
```

## Troubleshooting

### Frontend won't start
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### API calls failing
- Check if backend is running on correct port
- Verify `VITE_API_BASE_URL` in `.env.local`
- Check browser console for CORS errors
- Verify API endpoints match PLAN.md contract

### Bot token issues
- Get token from Telegram BotFather
- Make sure token is in `src/bot/.env`
- Check token hasn't expired
- Verify bot hasn't been blocked by Telegram

## Architecture Overview

```
┌─────────────────┐
│  React Frontend │ (Port 5173)
│  - Dashboard    │
│  - Transactions │
│  - Charts       │
└────────┬────────┘
         │ HTTP API calls
         │
┌────────▼────────┐
│ FastAPI Backend │ (Port 8000)
│ - REST API      │
│ - Auth          │
│ - DB ORM        │
└────────┬────────┘
         │ SQL queries
         │
┌────────▼──────────────┐
│   PostgreSQL 15       │
│   - expenses table    │
│   - budgets table     │
│   - users table       │
└───────────────────────┘
         ▲
         │ Direct DB writes
         │
┌────────┴──────────────┐
│  Telegram Bot (CLI)   │
│ - Message handling    │
│ - Expense logging     │
│ - Budget checks       │
└───────────────────────┘
```

## Phase Implementation Status

- ✅ **Phase 1**: Infrastructure & DB Migration (Partially - SQLite → PostgreSQL pending)
- ✅ **Phase 2**: FastAPI Backend Scaffold (Not started)
- ⏳ **Phase 3**: API Endpoints & Business Logic (Pending backend)
- ✅ **Phase 4**: React Frontend (COMPLETE)
- ⏳ **Phase 5**: Polish & Deployment Prep (Pending)

## Next Steps

1. **Backend Development** (Phase 2-3)
   - Setup FastAPI project
   - Create database models with SQLAlchemy
   - Implement API endpoints
   - Setup authentication

2. **Frontend Polish**
   - Add authentication UI
   - Implement transaction CRUD
   - Complete budget management page
   - Add advanced analytics

3. **Integration & Testing**
   - Connect frontend to backend
   - Run end-to-end tests
   - Test bot + backend + frontend workflow

4. **Deployment**
   - Setup docker-compose.yml
   - Configure environment files
   - Deploy to production

## Support & Documentation

- **Frontend Docs**: `frontend/README.md`
- **Full Plan**: `PLAN.md`
- **Frontend Summary**: `FRONTEND_SUMMARY.md`
- **Bot Code**: `src/bot/`

## Quick Links

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000 (when available)
- API Docs: http://localhost:8000/docs (when available)
- Telegram: Start chat with your bot

---

**Last Updated**: 2026-04-29
**Frontend Status**: ✅ Phase 4 Complete
**Backend Status**: ⏳ Phase 2 Pending
