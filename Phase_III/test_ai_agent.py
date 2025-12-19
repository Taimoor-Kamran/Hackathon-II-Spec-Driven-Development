"""
Test script for the Todo AI Chatbot
"""

import asyncio
import os
from todo_ai_agent import TodoAIChatbot


async def test_chatbot():
    # Initialize the chatbot with the OpenAI API key from environment
    chatbot = TodoAIChatbot(
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        backend_url="http://localhost:8000",
    )

    print("Testing the Todo AI Chatbot...\n")

    # Test creating a task
    print("1. Testing task creation:")
    try:
        response = await chatbot.process_user_input(
            "Create a task to buy groceries", "test_user_123"
        )
        print(f"Response: {response}\n")
    except Exception as e:
        print(f"Error creating task: {e}\n")

    # Test listing tasks
    print("2. Testing task listing:")
    try:
        response = await chatbot.process_user_input(
            "What tasks do I have?", "test_user_123"
        )
        print(f"Response: {response}\n")
    except Exception as e:
        print(f"Error listing tasks: {e}\n")

    # Test updating a task (this would require knowing a task ID, so we'll try a generic update)
    print("3. Testing task update:")
    try:
        response = await chatbot.process_user_input(
            "Mark the groceries task as completed", "test_user_123"
        )
        print(f"Response: {response}\n")
    except Exception as e:
        print(f"Error updating task: {e}\n")

    # Test creating a category
    print("4. Testing category creation:")
    try:
        response = await chatbot.process_user_input(
            "Create a category called 'Work'", "test_user_123"
        )
        print(f"Response: {response}\n")
    except Exception as e:
        print(f"Error creating category: {e}\n")

    except Exception as e:
        print(f"Error creating category: {e}\n")

if __name__ == "__main__":
    asyncio.run(test_chatbot())
