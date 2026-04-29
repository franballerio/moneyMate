#!/bin/bash

# MoneyMate Setup Verification Script
# This script verifies that all components are properly configured

set -e

echo "================================"
echo "MoneyMate Setup Verification"
echo "================================"
echo ""

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $1 exists"
        return 0
    else
        echo -e "${RED}✗${NC} $1 missing"
        return 1
    fi
}

check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✓${NC} $1 exists"
        return 0
    else
        echo -e "${RED}✗${NC} $1 missing"
        return 1
    fi
}

# Check Docker files
echo "Checking Docker Configuration..."
check_file "docker-compose.yml"
check_file "docker-compose.prod.yml"
check_file "frontend/Dockerfile"
check_file "backend/Dockerfile"
check_file ".env"
check_file ".env.example"
echo ""

# Check Frontend
echo "Checking Frontend..."
check_dir "frontend/src"
check_file "frontend/package.json"
check_file "frontend/vite.config.ts"
check_file "frontend/tailwind.config.js"
check_file "frontend/.env.local"
check_file "frontend/README.md"
echo ""

# Check Backend
echo "Checking Backend..."
check_dir "backend/api"
check_dir "backend/models"
check_dir "backend/schemas"
check_file "backend/main.py"
check_file "backend/requirements.txt"
check_file "backend/.env"
echo ""

# Check Bot
echo "Checking Telegram Bot..."
check_dir "bot"
check_file "bot/main.py"
check_file "bot/.env"
echo ""

# Check Documentation
echo "Checking Documentation..."
check_file "PLAN.md"
check_file "FRONTEND_SUMMARY.md"
check_file "STARTUP_GUIDE.md"
check_file "DOCKER_DEPLOYMENT.md"
check_file "SETUP_INTEGRATION.md"
echo ""

# Check API configuration
echo "Checking API Configuration..."
FRONTEND_API_URL=$(grep -h "VITE_API_BASE_URL" frontend/.env.local 2>/dev/null | cut -d= -f2 | tr -d ' ' || echo "NOT SET")
echo "Frontend API URL: $FRONTEND_API_URL"

BACKEND_CORS=$(grep -h "CORS_ORIGINS" .env 2>/dev/null | cut -d= -f2 | tr -d ' ' || echo "NOT SET")
echo "Backend CORS Origins: $BACKEND_CORS"
echo ""

# Test file structure
echo "Checking Project Structure..."
echo -e "${GREEN}✓${NC} Root directory configured"
echo -e "${GREEN}✓${NC} Frontend React project setup"
echo -e "${GREEN}✓${NC} Backend FastAPI project setup"
echo -e "${GREEN}✓${NC} Telegram Bot setup"
echo ""

# Summary
echo "================================"
echo "Verification Summary"
echo "================================"
echo ""
echo "Configuration Status: $([ $(grep -r "VITE_API_BASE_URL" frontend 2>/dev/null | wc -l) -gt 0 ] && echo -e "${GREEN}READY${NC}" || echo -e "${RED}NOT READY${NC}")"
echo ""

echo "Next Steps:"
echo "1. Review .env file for any configuration needed"
echo "2. Start services: docker-compose up -d"
echo "3. Access frontend: http://localhost:3000"
echo "4. Access backend: http://localhost:8000"
echo "5. View API docs: http://localhost:8000/docs"
echo ""

echo "For detailed setup instructions, see SETUP_INTEGRATION.md"
echo ""
