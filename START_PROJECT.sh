#!/bin/bash

# Script to start the AI DevOps Pipeline

echo "🚀 Starting AI-Powered DevOps Pipeline..."
echo ""

# Activate virtual environment
source venv/bin/activate

# Start backend
echo "✅ Starting Backend Server..."
echo "📍 Backend will run on: http://localhost:8000"
echo ""
python3 -m backend.main
