#!/bin/bash

# Script to start BOTH backend and frontend together

echo "🚀 Starting AI-Powered DevOps Pipeline..."
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if setup was done
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment not found!${NC}"
    echo "Please run ./QUICK_START.sh first!"
    exit 1
fi

if [ ! -d "frontend/node_modules" ]; then
    echo -e "${YELLOW}⚠️  Frontend dependencies not found!${NC}"
    echo "Please run ./QUICK_START.sh first!"
    exit 1
fi

echo -e "${BLUE}Starting Backend Server...${NC}"
echo "📍 Backend: http://localhost:8000"
echo ""

# Start backend in background
source venv/bin/activate
python3 -m backend.main &
BACKEND_PID=$!

echo -e "${GREEN}✓${NC} Backend started (PID: $BACKEND_PID)"
echo ""

# Wait 3 seconds for backend to start
sleep 3

echo -e "${BLUE}Starting Frontend Server...${NC}"
echo "📍 Frontend: http://localhost:3000"
echo ""

# Start frontend in background
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo -e "${GREEN}✓${NC} Frontend started (PID: $FRONTEND_PID)"
echo ""
echo -e "${GREEN}============================================${NC}"
echo -e "${GREEN}🎉 Both servers are running!${NC}"
echo -e "${GREEN}============================================${NC}"
echo ""
echo -e "${BLUE}Open in browser:${NC} http://localhost:3000"
echo ""
echo -e "${BLUE}Login credentials:${NC}"
echo "  Username: iamjitishkr"
echo "  Password: jitish123"
echo ""
echo -e "${YELLOW}To stop both servers:${NC}"
echo "  Press Ctrl+C, then run: kill $BACKEND_PID $FRONTEND_PID"
echo ""
echo -e "${BLUE}Logs:${NC}"
echo "  Backend: Terminal will show FastAPI logs"
echo "  Frontend: Terminal will show Vite logs"
echo ""

# Wait for user to press Ctrl+C
trap "echo ''; echo '🛑 Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo '✅ Stopped!'; exit 0" INT

echo "Press Ctrl+C to stop both servers..."
echo ""

# Keep script running and show logs
wait
