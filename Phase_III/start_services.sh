#!/bin/bash

# Start the Todo AI Chatbot services
# This script starts both the MCP server and the main backend service

echo "Starting Todo AI Chatbot services..."

# Create a virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Start the MCP server in the background
echo "Starting MCP server..."
python mcp_server.py 8080 &
MCP_PID=$!

# Give the MCP server a moment to start
sleep 2

# Start the main backend service
echo "Starting main backend service..."
python main.py

# Cleanup function
cleanup() {
    echo "Shutting down services..."
    kill $MCP_PID 2>/dev/null
    exit 0
}

# Set up signal trapping to clean up on exit
trap cleanup INT TERM

# Wait for processes to finish
wait