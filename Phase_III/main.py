"""
Main entry point for Todo AI Chatbot
Runs the FastAPI backend service
"""

import asyncio
import uvicorn
from chat_endpoint import app
from mcp_server import create_db_and_tables


def main():
    """Main entry point"""
    # Initialize database tables
    create_db_and_tables()

    print("Starting Todo AI Chatbot backend service...")
    print("Database initialized, starting server on port 8000...")

    # Run the FastAPI app with uvicorn
    uvicorn.run(
        "chat_endpoint:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )


if __name__ == "__main__":
    main()