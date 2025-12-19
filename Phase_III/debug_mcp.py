#!/usr/bin/env python3
"""
Test script to debug MCP server communication
"""
import asyncio
import json
import subprocess
import sys

async def debug_mcp_server():
    print("Starting MCP server subprocess...")

    # Start the MCP server as a subprocess
    process = await asyncio.create_subprocess_exec(
        sys.executable, "-u", "/home/taimoor/Hackathon_II/Phase_III/mcp_server.py",
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    reader = process.stdout
    writer = process.stdin

    # Give the server a moment to initialize
    await asyncio.sleep(0.5)

    print("Server started, checking for any initial output...")
    # Try to read any initial output from the server
    try:
        initial_output = await asyncio.wait_for(reader.read(1024), timeout=1.0)
        if initial_output:
            print("Initial server output:", initial_output.decode())
        else:
            print("No initial output from server")
    except asyncio.TimeoutError:
        print("No initial output from server within timeout")

    print("\nSending tool listing request...")
    # Try to list tools first to see if the server responds
    list_tools_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/list"
    }

    request_str = json.dumps(list_tools_request) + "\n"
    print("Request sent:", request_str.strip())
    writer.write(request_str.encode())
    await writer.drain()

    # Read response
    try:
        response = await asyncio.wait_for(reader.read(4096), timeout=2.0)
        if response:
            response_str = response.decode()
            print("Response received:", response_str)
        else:
            print("No response data received")
    except asyncio.TimeoutError:
        print("No response received within timeout for tools/list")

    print("\nSending direct tool call request...")
    # Now try to call a tool directly
    tool_request = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": "list_tasks",
            "arguments": {"user_id": "test_user_123"}
        }
    }

    request_str = json.dumps(tool_request) + "\n"
    print("Request sent:", request_str.strip())
    writer.write(request_str.encode())
    await writer.drain()

    # Read response
    try:
        response = await asyncio.wait_for(reader.read(4096), timeout=2.0)
        if response:
            response_str = response.decode()
            print("Response received:", response_str)
        else:
            print("No response data received for tool call")
    except asyncio.TimeoutError:
        print("No response received within timeout for tool call")

    # Check stderr for any error messages
    try:
        stderr_output = await asyncio.wait_for(process.stderr.read(1024), timeout=0.5)
        if stderr_output:
            print("STDERR output:", stderr_output.decode())
    except asyncio.TimeoutError:
        pass

    # Close connections
    writer.close()
    await writer.wait_closed()
    process.terminate()
    await process.wait()

    print("\nTest completed.")

if __name__ == "__main__":
    asyncio.run(debug_mcp_server())