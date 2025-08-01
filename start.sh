#!/bin/bash

# AskAfrica - Start Script
# This script starts both the backend and frontend services

echo "🚀 Starting AskAfrica..."

# Function to check if a port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        echo "⚠️  Port $1 is already in use"
        return 1
    else
        return 0
    fi
}

# Check if Ollama is running
if ! curl -s http://localhost:11434 >/dev/null; then
    echo "❌ Ollama is not running. Please start Ollama first:"
    echo "   ollama serve"
    exit 1
fi

echo "✅ Ollama is running"

# Start backend
echo "🔧 Starting backend..."
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment and install dependencies
source venv/bin/activate
pip install -r requirements.txt >/dev/null 2>&1

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cp .env.template .env
fi

# Start backend in background
if check_port 8000; then
    echo "🌐 Backend starting on http://localhost:8000"
    uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
    BACKEND_PID=$!
    echo "📊 Backend PID: $BACKEND_PID"
else
    echo "❌ Backend port 8000 is already in use"
    exit 1
fi

# Wait a moment for backend to start
sleep 3

# Start frontend
echo "🎨 Starting frontend..."
cd ../frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    npm install >/dev/null 2>&1
fi

# Check if frontend port is available
if check_port 3000; then
    echo "🌐 Frontend starting on http://localhost:3000"
    npm run dev &
    FRONTEND_PID=$!
    echo "📊 Frontend PID: $FRONTEND_PID"
else
    echo "❌ Frontend port 3000 is already in use"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

echo ""
echo "🎉 AskAfrica is starting up!"
echo ""
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend:  http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping services..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ Services stopped"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Wait for user to stop
wait 