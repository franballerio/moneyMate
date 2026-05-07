# PLAN.md — MoneyMate Full-Stack Expansion

## META
- Project: MoneyMate
- Migration: Telegram bot (SQLite) → Full-stack app (PostgreSQL + FastAPI + React)
- Architecture: N-Tier Monorepo
- Status: Planning

---

## STRUCTURE

```mermaid
graph TD
    ROOT["moneyMate/"]
    ROOT --> BOT["bot/  ← existing code, updated for PostgreSQL"]
    ROOT --> FE["frontend/  ← React + Vite + TailwindCSS"]
    ROOT --> BE["backend/  ← FastAPI"]
    ROOT --> DC["docker-compose.yml"]
    BE --> BE_MAIN["main.py  ← entry point, CORS"]
    BE --> BE_API["api/  ← routers"]
    BE --> BE_CORE["core/  ← config, DB engine"]
    BE --> BE_MODELS["models/  ← SQLAlchemy ORM"]
    BE --> BE_SCHEMAS["schemas/  ← Pydantic"]
    BE --> BE_SERVICES["services/  ← business logic"]
    BE --> BE_REPOS["repositories/  ← CRUD abstraction"]
```

---

## ARCHITECTURE

```mermaid
flowchart LR
    BOT["Telegram Bot\nPython + psycopg2\nDirect DB writes"]
    FE["React Frontend\nAxios REST calls"]
    BE["FastAPI Backend\nSQLAlchemy ORM"]
    DB[("PostgreSQL 15\nDocker: moneymate_db")]

    BOT -->|psycopg2| DB
    FE -->|HTTP /api/v1| BE
    BE -->|SQLAlchemy| DB
```

---

## PHASES

```mermaid
flowchart TD
    P1["PHASE 1\nInfrastructure"] --> P2["PHASE 2\nFastAPI Setup"]
    P2 --> P3["PHASE 3\nAPI + Business Logic"]
    P3 --> P4["PHASE 4\nReact Dashboard"]
    P4 --> P5["PHASE 5\nPolish + Deployment Prep"]
```

### PHASE 1 — Infrastructure & DB Migration
```mermaid
flowchart TD
    A["Create monorepo dirs"] --> B["Move bot → bot/"]
    B --> C["docker-compose.yml\nimage: postgres:15\ndb: moneymate_db"]
    C --> D["pip install psycopg2-binary"]
    D --> E["Swap sqlite3 → psycopg2 in bot"]
    E --> F["Refactor SQL: ? placeholders → %s"]
```

### PHASE 2 — FastAPI Backend Scaffold
```mermaid
flowchart TD
    A["python -m venv backend/venv"] --> B["pip install\nfastapi uvicorn sqlalchemy\npsycopg2-binary pydantic\nalembic python-dotenv"]
    B --> C["core/database.py\nSQLAlchemy engine → PostgreSQL"]
    C --> D["alembic init\nSchema migration tracking"]
    D --> E["models/expense.py\nORM mirrors bot table schema"]
    E --> F["schemas/expense.py\nPydantic request+response models"]
```

### PHASE 3 — API Endpoints & Business Logic
```mermaid
flowchart TD
    REPO["repositories/expense_repo.py\nMethods: get_all · get_by_date · get_by_category"]
    SVC["services/metrics_service.py\nBusiness rule: FX rate = 1500 (fixed, non-configurable)"]
    REPO --> SVC
    SVC --> R1["GET /api/v1/expenses\npaginated expense list"]
    SVC --> R2["GET /api/v1/metrics/summary\ntotals: daily · monthly · all-time"]
    SVC --> R3["GET /api/v1/metrics/categories\ngrouped spend per category"]
    SVC --> R4["GET /api/v1/metrics/trends\nchronological spend series"]
    R1 & R2 & R3 & R4 --> CORS["main.py\nCORS: allow React origin"]
```

### PHASE 4 — React Frontend
```mermaid
flowchart TD
    A["npm create vite@latest frontend/\n--template react-ts"] --> B["npm install\naxios recharts tailwindcss react-router-dom"]
    B --> C["axios instance\nbaseURL: http://localhost:8000/api/v1"]
    C --> D["Layout: Sidebar + Header"]
    C --> E["Dashboard: metric cards + budget progress"]
    C --> F["Charts:\n  Line → daily trends\n  Pie  → category breakdown"]
    C --> G["Transactions: table + filter + pagination"]
    D & E & F & G --> H["Wire all components to API endpoints"]
```

### PHASE 5 — Polish & Deployment Prep
```mermaid
flowchart TD
    A["Verify concurrent access\nBot + Backend → same PostgreSQL"] --> B["Add .env.example\nto bot/ and backend/"]
    B --> C["Update README.md\nLocal startup: DB → backend → frontend → bot"]
```

---

## API CONTRACT

```mermaid
graph LR
    CLIENT["React / Axios"]
    CLIENT --> EP1["GET /api/v1/expenses\nQuery: page, limit\nReturns: paginated ExpenseList"]
    CLIENT --> EP2["GET /api/v1/metrics/summary\nReturns: {daily, monthly, all_time}"]
    CLIENT --> EP3["GET /api/v1/metrics/categories\nReturns: [{category, total}]  ← pie chart"]
    CLIENT --> EP4["GET /api/v1/metrics/trends\nReturns: [{date, total}]  ← line/bar chart"]
```

---

## TECH STACK

| Layer      | Technology                                      |
|------------|-------------------------------------------------|
| Database   | PostgreSQL 15 (Docker)                          |
| Backend    | Python, FastAPI, SQLAlchemy, Alembic, Pydantic  |
| Frontend   | React, Vite, TypeScript, TailwindCSS, Recharts  |
| Bot        | Python, python-telegram-bot, psycopg2           |

---

## KEY CONSTRAINTS
- FX conversion rate: `1500` — hardcoded in `services/metrics_service.py`, applied to all metric aggregations
- Bot and backend share the same PostgreSQL instance; writes must not conflict
- SQL placeholder syntax: `%s` (psycopg2), not `?` (sqlite3)
- CORS must explicitly allow the React dev origin (`http://localhost:5173`)
- All schema migrations managed by Alembic — no manual DDL after Phase 2

---

## IMPROVEMENTS & ENHANCEMENTS NEEDED

### 1. Error Handling & Validation Strategy
- **API Error Responses:** Define standard HTTP error codes (400 for validation, 404 for not found, 500 for server errors)
- **Input Validation:** Validate expense amounts (must be > 0), date ranges, and category names
- **Database Error Handling:** Graceful recovery from PostgreSQL connection failures, timeouts, and deadlocks
- **Logging Strategy:** Use Python logging module; log all API calls, DB operations, and errors with severity levels

### 2. Authentication & Authorization
- **User Authentication:** Implement JWT-based authentication for React frontend (login/register endpoints)
- **User Isolation:** Each expense record must have a `user_id` foreign key; all queries filtered by authenticated user
- **Telegram Bot Auth:** Generate secure API tokens for bot; bot provides token in connection string or headers
- **Role-Based Access Control (RBAC):** Support admin/user roles (future-proofing for shared budgets)
- **Password Security:** Hash passwords with bcrypt; implement password reset flow

### 3. Data Integrity & Concurrency
- **Transaction Management:** Wrap multi-step operations (insert expense + update budget) in database transactions
- **Optimistic Locking:** Add `version` field to expense/budget records to detect concurrent modifications
- **Row-Level Locks:** Use PostgreSQL's `FOR UPDATE` clause when bot and backend access same record
- **Conflict Resolution Strategy:** Define behavior when bot and backend write simultaneously (last-write-wins vs. queue)
- **Connection Pooling:** Use SQLAlchemy's connection pooling to manage concurrent DB access efficiently

### 4. Testing Strategy
- **Unit Tests:** Test business logic (metrics_service.py, repositories) with mocked database
- **Integration Tests:** Test API endpoints with live PostgreSQL test database
- **E2E Tests:** Test bot → DB → API → Frontend workflow
- **Test Fixtures:** Pre-seed test database with sample expenses, budgets, users
- **CI/CD Integration:** Run tests on every commit (GitHub Actions / GitLab CI)
- **Test Coverage Target:** Aim for 80%+ code coverage

### 5. Deployment & DevOps
- **docker-compose.yml Details:**
  - PostgreSQL service: image `postgres:15`, environment vars (POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB)
  - Backend service: build from Dockerfile, port 8000, environment vars (DATABASE_URL, SECRET_KEY)
  - Frontend service: nginx reverse proxy, port 80, build production bundle
  - Volumes: PostgreSQL data persistence (`./data/postgres`), environment files
  - Networks: internal network for service-to-service communication
- **Frontend Build:** Separate Dockerfile for React; use multi-stage build (build → serve with nginx)
- **Environment Files:** Create `docker-compose.override.yml` for local dev settings
- **Database Backup:** Scheduled PostgreSQL backups using pg_dump; store in cloud storage
- **Production Secrets:** Use environment variables from CI/CD secrets manager (GitHub Secrets, GitLab CI variables)
- **Database Migrations:** Alembic migrations run automatically on backend startup

### 6. Extended API Design
- **Complete CRUD for Expenses:**
  - `POST /api/v1/expenses` — Create new expense (with validation)
  - `PUT /api/v1/expenses/{id}` — Update existing expense
  - `DELETE /api/v1/expenses/{id}` — Soft-delete expense (mark deleted_at timestamp)
  - `GET /api/v1/expenses/{id}` — Fetch single expense
- **Expense Filtering & Pagination:**
  - Query params: `?page=1&limit=20&start_date=2024-01-01&end_date=2024-01-31&category=food`
  - Response includes total count, current page, total pages
- **Budget Endpoints:**
  - `GET /api/v1/budgets` — List all budgets for user
  - `POST /api/v1/budgets` — Create budget with category and limit
  - `PUT /api/v1/budgets/{id}` — Update budget limit
  - `DELETE /api/v1/budgets/{id}` — Delete budget
  - `GET /api/v1/budgets/{id}/progress` — Get budget utilization (spent vs. limit)
- **Category Endpoints:**
  - `GET /api/v1/categories` — List all categories (with color/icon metadata)
  - `POST /api/v1/categories` — Create custom category
- **Consistent Response Format:**
  ```json
  {
    "success": true,
    "data": {...},
    "error": null,
    "timestamp": "2024-01-15T10:30:00Z"
  }
  ```

### 7. Frontend Specifics
- **Authentication UI:**
  - Login page with email/password form
  - Register/signup page
  - "Forgot password" flow
  - User profile settings page
  - Logout functionality
- **Real-Time Updates:**
  - Option 1 (Simple): Frontend polls API every 5-10 seconds
  - Option 2 (Advanced): Implement WebSocket for live updates from bot
  - Use React Query (`useQuery`) with refetch intervals
- **Offline Support:**
  - Use localStorage to cache recent expenses
  - Queue new expenses when offline; sync on reconnect
  - Service Worker for offline PWA support (future)
- **Transaction UI:**
  - Form to create/edit/delete expenses
  - Quick-add button with category pre-selection
  - Bulk import (CSV upload)
  - Transaction detail modal with edit/delete actions
- **Data Visualization:**
  - Charts use recharts library with responsive sizing
  - Daily trend line chart
  - Category pie/donut chart
  - Budget progress bars
  - Month-to-date vs. budget comparison

### 8. Database Schema (PostgreSQL)
- **users table:**
  ```sql
  id UUID PRIMARY KEY
  email VARCHAR UNIQUE NOT NULL
  password_hash VARCHAR NOT NULL
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  ```
- **expenses table:**
  ```sql
  id UUID PRIMARY KEY
  user_id UUID NOT NULL FOREIGN KEY → users
  amount DECIMAL(12,2) NOT NULL
  category VARCHAR NOT NULL
  description TEXT
  date DATE NOT NULL
  created_by VARCHAR ('bot' | 'web') NOT NULL
  version INT DEFAULT 1 (for optimistic locking)
  deleted_at TIMESTAMP NULL (soft delete)
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  ```
- **budgets table:**
  ```sql
  id UUID PRIMARY KEY
  user_id UUID NOT NULL FOREIGN KEY → users
  category VARCHAR NOT NULL
  limit_amount DECIMAL(12,2) NOT NULL
  period VARCHAR ('monthly' | 'yearly') DEFAULT 'monthly'
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  ```
- **Indexes:** Add composite indexes on (user_id, date), (user_id, category) for query performance

### 9. Environment & Configuration
- **Backend .env.example:**
  ```
  DATABASE_URL=postgresql://user:password@localhost:5432/moneymate
  SECRET_KEY=your-secret-key-here
  JWT_EXPIRATION_HOURS=24
  CORS_ORIGINS=http://localhost:5173,http://localhost:3000
  LOG_LEVEL=INFO
  ENVIRONMENT=development
  ```
- **Bot .env.example:**
  ```
  TELEGRAM_BOT_TOKEN=your-token-here
  DATABASE_URL=postgresql://user:password@localhost:5432/moneymate
  BOT_API_TOKEN=secure-token-for-bot-identification
  LOG_LEVEL=INFO
  ```
- **Frontend .env.example:**
  ```
  VITE_API_BASE_URL=http://localhost:8000/api/v1
  VITE_ENVIRONMENT=development
  ```
- **Multi-Environment Support:**
  - `.env.development` — local development settings
  - `.env.staging` — staging environment
  - `.env.production` — production (loaded from secrets manager)

### 10. Documentation & API Documentation
- **OpenAPI/Swagger:**
  - FastAPI auto-generates Swagger docs at `/docs`
  - Include all endpoints, request/response schemas, error codes
  - Mark deprecated endpoints clearly
- **Entity-Relationship Diagram (ERD):**
  - Visualize users ↔ expenses ↔ budgets relationships
  - Show foreign keys and constraints
- **Developer Setup Guide (README.md):**
  - Prerequisites (Python 3.9+, Node 16+, Docker)
  - Step-by-step local setup: `docker-compose up`, `pip install -r requirements.txt`, `npm install`
  - How to run migrations: `alembic upgrade head`
  - How to seed test data
  - How to run tests: `pytest`
  - How to start services: backend, frontend, bot
- **API Documentation:**
  - Link to Swagger docs in README
  - Example curl/Postman requests for each endpoint
  - Common error scenarios and solutions

### 11. User Isolation & Multi-User Considerations
- **Decision:** Should this support multiple users sharing a household budget or individual user budgets?
- **If individual budgets:** Each user logs in separately; all data filtered by `user_id`
- **If shared household:** Consider shared expense categories, family roles, approval workflows
- **User Signup:** Allow self-registration or admin-invite only?
- **Bot Integration:** Should bot associate expenses with a specific user or a "system" user?

### 12. Real-Time Bot-Frontend Sync
- **Option 1 (Polling):** Frontend calls `/api/v1/expenses?since=<last_update>` periodically
- **Option 2 (WebSocket):** Bot publishes message to Redis pub/sub; backend broadcasts to connected clients
- **Option 3 (Webhooks):** Bot sends HTTP webhook to backend; backend notifies frontend via WebSocket

### 13. Alembic & Schema Versioning
- **Migration Workflow:**
  - Developer makes model changes in `models/expense.py`
  - Run `alembic revision --autogenerate -m "Add user_id to expenses"`
  - Review generated migration file for correctness
  - Test locally: `alembic upgrade head`
  - Commit migration file; it runs automatically on production startup
- **Rollback Plan:** Document how to rollback migrations if needed (`alembic downgrade -1`)

### 14. Monitoring & Observability
- **Application Metrics:** Track API response times, error rates, DB query performance
- **Logging:** Structured JSON logs (requests, errors, bot actions)
- **Error Tracking:** Use Sentry or similar for production error monitoring
- **Database Monitoring:** Monitor PostgreSQL connection count, slow queries, disk usage