"""
AI Agent for Todo Chatbot
Uses OpenAI function calling to process natural language and interact with backend API
"""

import os
import json
import httpx
from typing import List, Dict, Any
from openai import OpenAI
from datetime import datetime


class TodoAIChatbot:
    def __init__(self, openai_api_key: str, backend_url: str = "http://localhost:8000"):
        """
        Initialize the Todo AI Chatbot using OpenAI function calling

        Args:
            openai_api_key: OpenAI API key for the agent
            backend_url: URL of the backend API
        """
        # Initialize the OpenAI client
        self.client = OpenAI(api_key=openai_api_key)

        # Store the backend URL for API calls
        self.backend_url = backend_url

        # Define tools that the agent can use (these mirror the backend API endpoints)
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "list_tasks",
                    "description": "List all tasks for the user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The user ID"}
                        },
                        "required": ["user_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "create_task",
                    "description": "Create a new task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The user ID"},
                            "title": {"type": "string", "description": "The title of the task"},
                            "description": {"type": "string", "description": "Optional description of the task"},
                            "category_id": {"type": "integer", "description": "Optional category ID"},
                            "due_date": {"type": "string", "description": "Optional due date in YYYY-MM-DD format"},
                            "priority": {"type": "string", "description": "Priority level (low, medium, high)"}
                        },
                        "required": ["user_id", "title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_task",
                    "description": "Update an existing task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "integer", "description": "The ID of the task to update"},
                            "user_id": {"type": "string", "description": "The user ID"},
                            "title": {"type": "string", "description": "New title (optional)"},
                            "description": {"type": "string", "description": "New description (optional)"},
                            "completed": {"type": "boolean", "description": "New completion status (optional)"},
                            "category_id": {"type": "integer", "description": "New category ID (optional)"},
                            "due_date": {"type": "string", "description": "New due date (optional)"},
                            "priority": {"type": "string", "description": "New priority level (optional)"}
                        },
                        "required": ["task_id", "user_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "description": "Delete a task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "integer", "description": "The ID of the task to delete"},
                            "user_id": {"type": "string", "description": "The user ID"}
                        },
                        "required": ["task_id", "user_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_all_tasks",
                    "description": "Delete all tasks for the user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The user ID"}
                        },
                        "required": ["user_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_categories",
                    "description": "List all categories for the user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The user ID"}
                        },
                        "required": ["user_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "create_category",
                    "description": "Create a new category",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The user ID"},
                            "name": {"type": "string", "description": "The name of the category"},
                            "color": {"type": "string", "description": "Hex color code for the category"}
                        },
                        "required": ["user_id", "name"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_tags",
                    "description": "List all tags for the user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The user ID"}
                        },
                        "required": ["user_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "create_tag",
                    "description": "Create a new tag",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The user ID"},
                            "name": {"type": "string", "description": "The name of the tag"}
                        },
                        "required": ["user_id", "name"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_all_tasks",
                    "description": "Delete all tasks for the user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The user ID"}
                        },
                        "required": ["user_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_all_categories",
                    "description": "Delete all categories for the user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The user ID"}
                        },
                        "required": ["user_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_all_tags",
                    "description": "Delete all tags for the user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The user ID"}
                        },
                        "required": ["user_id"]
                    }
                }
            }
        ]

        self.conversation_history = []

    async def process_user_input(self, user_input: str, user_id: str) -> str:
        """
        Process user input and return appropriate response using OpenAI function calling
        This simulates the behavior of the OpenAI Agents SDK by using function calling

        Args:
            user_input: Natural language input from user
            user_id: ID of the user

        Returns:
            AI-generated response
        """
        # Prepare the messages for the AI - only include recent conversation to avoid invalid sequences
        messages = [
            {
                "role": "system",
                "content": f"""You are an AI assistant that helps users manage their tasks using natural language.
                Use the provided tools to interact with the task management system.
                Always be helpful and provide clear, concise responses.
                The current user ID is: {user_id}
                Always use this user ID when making tool calls.
                IMPORTANT: When a user refers to a task by position (like "task #1", "task #2", etc.), you MUST follow these exact steps:
                1. FIRST: Call the list_tasks function with the user ID to get the current task list and their database IDs
                2. SECOND: Identify which database ID corresponds to the positional reference (e.g., if user says "task #1", find the database ID of the first task in the list)
                3. THIRD: Perform the requested operation (update, delete, etc.) using the CORRECT database ID
                EXAMPLE: If user says "Mark task #1 as complete":
                - Step 1: Call list_tasks to see all tasks and their database IDs
                - Step 2: Identify that the first task in the list has database ID X
                - Step 3: Call update_task with task_id: X and completed: true
                This sequence is mandatory. Never skip step 1 or step 2.
                If a user asks to list tasks, use the list_tasks function with the correct user ID.
                If a user asks to create a task, use the create_task function with the correct user ID.
                If a user asks to update a task, first call list_tasks to identify the correct database ID, then use the update_task function with the correct user ID and database ID.
                If a user asks to delete a task, first call list_tasks to identify the correct database ID, then use the delete_task function with the correct user ID and database ID.
                If a user asks about categories, use the appropriate category functions with the correct user ID.
                If a user asks about tags, use the appropriate tag functions with the correct user ID."""
            }
        ]

        # Only add recent conversation history that doesn't contain tool messages
        # to avoid invalid message sequences
        recent_history = []
        for msg in self.conversation_history[-10:]:  # Only last 10 messages
            # Only add user and assistant messages, not tool messages
            if msg["role"] in ["user", "assistant"]:
                recent_history.append(msg)

        messages.extend(recent_history)

        # Add the current user input
        messages.append({"role": "user", "content": user_input})

        # Call the OpenAI API with tool calling (this is the modern equivalent of Agents SDK)
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",  # Using a model that's generally available
            messages=messages,
            tools=self.tools,
            tool_choice="auto"
        )

        # Process the response
        response_message = response.choices[0].message

        # Handle tool calls if any
        tool_calls = response_message.tool_calls
        if tool_calls:
            # For OpenAI API, we need to separate the initial call from the tool results
            # Build temporary messages for this specific interaction only
            temp_messages = [
                {"role": "system", "content": f"""You are an AI assistant that helps users manage their tasks using natural language.
                Use the provided tools to interact with the task management system.
                Always be helpful and provide clear, concise responses.
                The current user ID is: {user_id}
                Always use this user ID when making tool calls."""},
            ]

            # Add recent history without tool messages
            for msg in recent_history:
                temp_messages.append(msg)

            # Add the current user input and assistant's tool call request
            temp_messages.append({"role": "user", "content": user_input})
            temp_messages.append(response_message)

            # Execute each tool call using HTTP requests to the backend API
            tool_results = []
            async with httpx.AsyncClient() as client:
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)

                    # Override the user_id to ensure it's always the correct one
                    # This fixes the issue where AI model might extract wrong user_id
                    function_args['user_id'] = user_id

                    # Execute the function using HTTP requests to backend API
                    try:
                        if function_name == "list_tasks":
                            response = await client.get(f"{self.backend_url}/api/{function_args['user_id']}/tasks")
                            result = response.json() if response.status_code == 200 else {"error": f"HTTP {response.status_code}: {response.text}"}
                        elif function_name == "create_task":
                            response = await client.post(
                                f"{self.backend_url}/api/{function_args['user_id']}/tasks",
                                json={
                                    "title": function_args.get("title"),
                                    "description": function_args.get("description"),
                                    "category_id": function_args.get("category_id"),
                                    "due_date": function_args.get("due_date"),
                                    "priority": function_args.get("priority", "medium")
                                }
                            )
                            result = response.json() if response.status_code == 200 else {"error": f"HTTP {response.status_code}: {response.text}"}
                        elif function_name == "update_task":
                            # Only include fields that are explicitly provided to avoid NULL constraint issues
                            update_data = {}
                            if "title" in function_args and function_args["title"] is not None:
                                update_data["title"] = function_args["title"]
                            if "description" in function_args and function_args["description"] is not None:
                                update_data["description"] = function_args["description"]
                            if "completed" in function_args and function_args["completed"] is not None:
                                update_data["completed"] = function_args["completed"]
                            if "category_id" in function_args and function_args["category_id"] is not None:
                                update_data["category_id"] = function_args["category_id"]
                            if "due_date" in function_args and function_args["due_date"] is not None:
                                update_data["due_date"] = function_args["due_date"]
                            if "priority" in function_args and function_args["priority"] is not None:
                                update_data["priority"] = function_args["priority"]

                            response = await client.put(
                                f"{self.backend_url}/api/{function_args['user_id']}/tasks/{function_args['task_id']}",
                                json=update_data
                            )
                            result = response.json() if response.status_code == 200 else {"error": f"HTTP {response.status_code}: {response.text}"}
                        elif function_name == "delete_task":
                            response = await client.delete(f"{self.backend_url}/api/{function_args['user_id']}/tasks/{function_args['task_id']}")
                            result = response.json() if response.status_code == 200 else {"error": f"HTTP {response.status_code}: {response.text}"}
                        elif function_name == "delete_all_tasks":
                            response = await client.delete(f"{self.backend_url}/api/{function_args['user_id']}/tasks")
                            result = response.json() if response.status_code == 200 else {"error": f"HTTP {response.status_code}: {response.text}"}
                        elif function_name == "delete_all_categories":
                            response = await client.delete(f"{self.backend_url}/api/{function_args['user_id']}/categories")
                            result = response.json() if response.status_code == 200 else {"error": f"HTTP {response.status_code}: {response.text}"}
                        elif function_name == "delete_all_tags":
                            response = await client.delete(f"{self.backend_url}/api/{function_args['user_id']}/tags")
                            result = response.json() if response.status_code == 200 else {"error": f"HTTP {response.status_code}: {response.text}"}
                        elif function_name == "list_categories":
                            response = await client.get(f"{self.backend_url}/api/{function_args['user_id']}/categories")
                            result = response.json() if response.status_code == 200 else {"error": f"HTTP {response.status_code}: {response.text}"}
                        elif function_name == "create_category":
                            response = await client.post(
                                f"{self.backend_url}/api/{function_args['user_id']}/categories",
                                json={
                                    "name": function_args["name"],
                                    "color": function_args.get("color", "#000000")
                                }
                            )
                            result = response.json() if response.status_code == 200 else {"error": f"HTTP {response.status_code}: {response.text}"}
                        elif function_name == "list_tags":
                            response = await client.get(f"{self.backend_url}/api/{function_args['user_id']}/tags")
                            result = response.json() if response.status_code == 200 else {"error": f"HTTP {response.status_code}: {response.text}"}
                        elif function_name == "create_tag":
                            response = await client.post(
                                f"{self.backend_url}/api/{function_args['user_id']}/tags",
                                json={"name": function_args["name"]}
                            )
                            result = response.json() if response.status_code == 200 else {"error": f"HTTP {response.status_code}: {response.text}"}
                        else:
                            result = {"error": f"Unknown function: {function_name}"}
                    except Exception as e:
                        result = {"error": f"Error calling backend API: {str(e)}"}

                    # Add to tool results for the API call
                    tool_results.append({
                        "role": "tool",
                        "name": function_name,
                        "content": json.dumps(result),
                        "tool_call_id": tool_call.id
                    })

            # Add tool results to the temporary messages
            temp_messages.extend(tool_results)

            # Get the final response from the AI based on tool results
            final_response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=temp_messages  # Use clean temporary messages
            )

            final_content = final_response.choices[0].message.content

            # Only add user and assistant messages to the conversation history to avoid invalid sequences
            # The tool messages are only used for the current API call and not stored in history
            self.conversation_history.append({"role": "user", "content": user_input})
            self.conversation_history.append({"role": "assistant", "content": final_content})  # The final response after processing tools

            return final_content
        else:
            # No tool calls were made, return the content directly
            content = response_message.content
            # Add to conversation history before returning
            self.conversation_history.append({"role": "user", "content": user_input})
            self.conversation_history.append({"role": "assistant", "content": content})
            return content

    def clear_conversation_history(self):
        """Clear the conversation history"""
        self.conversation_history = []


# For testing purposes
if __name__ == "__main__":
    import asyncio

    async def test_chatbot():
        # Initialize the chatbot (using a placeholder API key)
        # In a real implementation, you would use a real OpenAI API key
        chatbot = TodoAIChatbot(openai_api_key=os.getenv("OPENAI_API_KEY", "placeholder"))

        print("Todo AI Chatbot initialized!")
        print("You can now interact with the chatbot by calling process_user_input()")
        print("\nExample usage:")
        print("response = await chatbot.process_user_input('Create a task to buy groceries', 'user123')")
        print("print(response)")

    # Run the test
    asyncio.run(test_chatbot())