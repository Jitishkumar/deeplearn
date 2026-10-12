#!/bin/bash

echo "🚀 AI-Powered DevOps Pipeline - Quick Start Script"
echo "=================================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Python is installed
echo -e "${BLUE}Checking prerequisites...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3.10 or higher.${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo -e "${GREEN}✓${NC} Python $PYTHON_VERSION found"

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is not installed. Please install Node.js 18 or higher.${NC}"
    exit 1
fi

NODE_VERSION=$(node --version)
echo -e "${GREEN}✓${NC} Node.js $NODE_VERSION found"

echo ""
echo -e "${BLUE}Step 1: Setting up Python virtual environment...${NC}"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓${NC} Virtual environment created"
else
    echo -e "${YELLOW}ℹ${NC} Virtual environment already exists"
fi

# Activate virtual environment
source venv/bin/activate

echo ""
echo -e "${BLUE}Step 2: Installing Python dependencies...${NC}"
pip install --quiet --upgrade pip
pip install --quiet -r backend/requirements.txt
echo -e "${GREEN}✓${NC} Python dependencies installed"

echo ""
echo -e "${BLUE}Step 3: Creating environment configuration...${NC}"
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${GREEN}✓${NC} .env file created"
else
    echo -e "${YELLOW}ℹ${NC} .env file already exists"
fi

echo ""
echo -e "${BLUE}Step 4: Initializing database...${NC}"
if [ ! -f "devops_pipeline.db" ]; then
    python -m backend.database.init_db
    echo -e "${GREEN}✓${NC} Database initialized with sample data"
else
    echo -e "${YELLOW}ℹ${NC} Database already exists. To reset, run: rm devops_pipeline.db && python -m backend.database.init_db"
fi

echo ""
echo -e "${BLUE}Step 5: Installing frontend dependencies...${NC}"
cd frontend
if [ ! -d "node_modules" ]; then
    npm install --silent
    echo -e "${GREEN}✓${NC} Frontend dependencies installed"
else
    echo -e "${YELLOW}ℹ${NC} Frontend dependencies already installed"
fi
cd ..

echo ""
echo -e "${GREEN}============================================${NC}"
echo -e "${GREEN}🎉 Setup Complete!${NC}"
echo -e "${GREEN}============================================${NC}"
echo ""
echo -e "${BLUE}To start the application:${NC}"
echo ""
echo -e "  ${YELLOW}Terminal 1 - Backend:${NC}"
echo "    cd /Users/jitishkumar/Desktop/amazonsde/deeplearn"
echo "    source venv/bin/activate"
echo "    python -m backend.main"
echo ""
echo -e "  ${YELLOW}Terminal 2 - Frontend:${NC}"
echo "    cd /Users/jitishkumar/Desktop/amazonsde/deeplearn/frontend"
echo "    npm run dev"
echo ""
echo -e "${BLUE}Then open:${NC} http://localhost:3000"
echo ""
echo -e "${BLUE}Login with:${NC}"
echo "  Username: demo"
echo "  Password: demo123"
echo ""
echo -e "${GREEN}Happy building! 🚀${NC}"
