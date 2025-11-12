#!/bin/bash

# Job Portal Startup Script
# This script stops any process using port 3000 and starts the Job Portal

echo "🔍 Checking for processes on port 3000..."

# Find and kill processes on port 3000
PORT_PIDS=$(lsof -ti:3000)

if [ ! -z "$PORT_PIDS" ]; then
    echo "⚠️  Found process(es) using port 3000: $PORT_PIDS"
    echo "🛑 Stopping these processes..."
    kill -9 $PORT_PIDS 2>/dev/null
    echo "✅ Port 3000 is now free"
else
    echo "✅ Port 3000 is already free"
fi

echo ""
echo "🚀 Starting Job Portal..."
echo "📦 Building and starting Docker containers..."
echo ""

# Start docker-compose
docker-compose up --build

# Note: Press Ctrl+C to stop the application

