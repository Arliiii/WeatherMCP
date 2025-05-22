"""
Example client for the OpenWeatherMap MCP server.
"""
import asyncio
from fastmcp import Client


async def main():
    """Connect to the MCP server and call the weather tools."""
    
    # Connect to the server
    async with Client("http://127.0.0.1:8000/mcp") as client:
        print("Connected to OpenWeatherMap MCP Server")
        
        # List available tools
        tools = await client.list_tools()
        print(f"Available tools: {[tool.name for tool in tools]}")
        
        # Get weather by city
        print("\n--- Weather by City ---")
        city_result = await client.call_tool(
            "get_weather_by_city", 
            {"city": "London", "country_code": "uk"}
        )
        print(city_result[0].text)
        
        # Get weather by coordinates
        print("\n--- Weather by Coordinates ---")
        coords_result = await client.call_tool(
            "get_weather_by_coordinates", 
            {"latitude": 40.7128, "longitude": -74.0060}
        )
        print(coords_result[0].text)
        
        # Get weather by zip code
        print("\n--- Weather by Zip Code ---")
        zip_result = await client.call_tool(
            "get_weather_by_zip", 
            {"zip_code": "94040", "country_code": "us"}
        )
        print(zip_result[0].text)
        
        # Read a resource
        print("\n--- Server Information ---")
        about_info = await client.read_resource("weather://about")
        print(about_info[0].text)


if __name__ == "__main__":
    asyncio.run(main())
