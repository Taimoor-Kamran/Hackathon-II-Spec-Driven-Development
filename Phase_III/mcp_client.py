"""
MCP Client for Todo operations
Connects to the MCP server to perform todo operations via stdio
"""
import asyncio
import json
from typing import List, Dict, Any
import subprocess
import sys


class MCPTodoClient:
    def __init__(self, mcp_server_path: str = "/home/taimoor/Hackathon_II/Phase_III/mcp_server.py"):
        """
        Initialize the MCP client for todo operations

        Args:
            mcp_server_path: Path to the MCP server script
        """
        self.mcp_server_path = mcp_server_path
        self.process = None
        self.reader = None
        self.writer = None

    async def __aenter__(self):
        """Start the MCP server process and initialize communication."""
        # Start the MCP server as a subprocess
        self.process = await asyncio.create_subprocess_exec(
            sys.executable, "-u", self.mcp_server_path,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        self.reader = self.process.stdout
        self.writer = self.process.stdin

        # Give the server a moment to initialize
        await asyncio.sleep(0.1)

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Close the connection and terminate the process."""
        if self.writer:
            self.writer.close()
            try:
                await self.writer.wait_closed()
            except:
                pass
        if self.process:
            self.process.terminate()
            try:
                await self.process.wait()
            except:
                pass

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Call an MCP tool with the given arguments."""
        if not self.writer:
            raise RuntimeError("MCP client not initialized. Use within async context manager.")

        # Create the MCP request
        request = {
            "jsonrpc": "2.0",
            "id": 1,  # Simple ID for this example
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }

        # Send the request
        request_str = json.dumps(request) + "\n"
        self.writer.write(request_str.encode())
        await self.writer.drain()

        # Read the response - the server might send multiple responses or in different format
        # Try to read and parse the response properly
        try:
            # Read a chunk of data that might contain the response
            response_data = await self.reader.read(4096)
            response_line = response_data.decode().strip()

            # The response might be in different format, let's try to extract JSON from it
            # Look for JSON object in the response
            import re
            json_match = re.search(r'\{.*\}', response_line, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                response = json.loads(json_str)

                if "error" in response:
                    raise Exception(f"MCP error: {response['error']}")

                return response.get("result", {})
            else:
                # If no JSON found, return an error
                raise Exception(f"No valid JSON response received. Got: {response_line}")
        except json.JSONDecodeError as e:
            # If JSON parsing fails, return an error
            raise Exception(f"Failed to parse JSON response: {e}. Response was: {response_data.decode() if 'response_data' in locals() else 'No data'}")
        except Exception as e:
            # Any other error
            raise Exception(f"Error reading MCP response: {e}")

    async def list_tasks(self, user_id: str) -> List[Dict[str, Any]]:
        """List all tasks for a user."""
        return await self.call_tool("list_tasks", {"user_id": user_id})

    async def create_task(self, user_id: str, title: str, description: str = None,
                         category_id: int = None, due_date: str = None,
                         priority: str = "medium") -> Dict[str, Any]:
        """Create a new task."""
        args = {
            "user_id": user_id,
            "title": title,
            "priority": priority
        }
        if description is not None:
            args["description"] = description
        if category_id is not None:
            args["category_id"] = category_id
        if due_date is not None:
            args["due_date"] = due_date

        return await self.call_tool("create_task", args)

    async def update_task(self, task_id: int, user_id: str, title: str = None,
                         description: str = None, completed: bool = None,
                         category_id: int = None, due_date: str = None,
                         priority: str = None) -> Dict[str, Any]:
        """Update an existing task."""
        args = {
            "task_id": task_id,
            "user_id": user_id
        }
        if title is not None:
            args["title"] = title
        if description is not None:
            args["description"] = description
        if completed is not None:
            args["completed"] = completed
        if category_id is not None:
            args["category_id"] = category_id
        if due_date is not None:
            args["due_date"] = due_date
        if priority is not None:
            args["priority"] = priority

        return await self.call_tool("update_task", args)

    async def delete_task(self, task_id: int, user_id: str) -> Dict[str, str]:
        """Delete a task."""
        return await self.call_tool("delete_task", {"task_id": task_id, "user_id": user_id})

    async def list_categories(self, user_id: str) -> List[Dict[str, Any]]:
        """List all categories for a user."""
        return await self.call_tool("list_categories", {"user_id": user_id})

    async def create_category(self, user_id: str, name: str, color: str = "#000000") -> Dict[str, Any]:
        """Create a new category."""
        args = {
            "user_id": user_id,
            "name": name
        }
        if color != "#000000":
            args["color"] = color

        return await self.call_tool("create_category", args)

    async def list_tags(self, user_id: str) -> List[Dict[str, Any]]:
        """List all tags for a user."""
        return await self.call_tool("list_tags", {"user_id": user_id})

    async def create_tag(self, user_id: str, name: str) -> Dict[str, Any]:
        """Create a new tag."""
        return await self.call_tool("create_tag", {"user_id": user_id, "name": name})


# Example usage
if __name__ == "__main__":
    async def main():
        # Example usage of the MCP client
        async with MCPTodoClient() as client:
            # Example: List tasks for a user
            tasks = await client.list_tasks("user123")
            print("Tasks:", tasks)

    # Run the example
    asyncio.run(main())