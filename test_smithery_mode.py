"""
Test script for the OpenWeatherMap MCP server in Smithery mode.

This script runs the server in stdio mode and sends a simple request to test functionality.
"""
import asyncio
import json
import os
import sys
import subprocess
from fastmcp import Client

async def test_server():
    """Test the server by connecting to it and calling a tool."""
    print("Starting OpenWeatherMap MCP server in stdio mode...")
    
    # Start the server process
    server_process = subprocess.Popen(
        [sys.executable, "server.py", "stdio"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=False
    )
    
    try:
        # Create a client that connects to the server process
        client = Client(server_process)
        
        print("Connecting to server...")
        async with client:
            print("Connected to server.")
            
            # List available tools
            tools = await client.list_tools()
            print(f"Available tools: {[tool.name for tool in tools]}")
            
            # Test get_weather_by_city tool with a sample city
            print("\nTesting get_weather_by_city tool...")
            try:
                result = await client.call_tool(
                    "get_weather_by_city", 
                    {"city": "London", "country_code": "uk"}
                )
                print("Result:")
                print(result[0].text)
                print("\nTest successful!")
            except Exception as e:
                print(f"Error calling tool: {e}")
                
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Terminate the server process
        server_process.terminate()
        try:
            server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_process.kill()

if __name__ == "__main__":
    # Check if API key is set
    if not os.environ.get("OPENWEATHER_API_KEY"):
        print("Error: OPENWEATHER_API_KEY environment variable is not set.")
        print("Please set it before running this test script.")
        sys.exit(1)
    
    # Run the test
    asyncio.run(test_server())
