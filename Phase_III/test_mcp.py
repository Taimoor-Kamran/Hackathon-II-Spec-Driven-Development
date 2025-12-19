import asyncio
from mcp_client import MCPTodoClient

async def test_mcp_connection():
    try:
        async with MCPTodoClient() as client:
            print("MCP client connected successfully")
            tasks = await client.list_tasks('test_user_123')
            print('Tasks:', tasks)
    except Exception as e:
        print(f"Error connecting to MCP: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_mcp_connection())