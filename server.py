"""
OpenWeatherMap MCP Server.

This server provides tools to interact with the OpenWeatherMap API
following the Model-Controller-Provider (MCP) architecture pattern.
"""
import os
import sys
from typing import Optional, Annotated
from fastmcp import FastMCP, Context
from pydantic import Field

from controller import WeatherController

# Initialize the FastMCP server
mcp = FastMCP(name="OpenWeatherMap MCP Server")

# Initialize the weather controller
weather_controller = WeatherController()


@mcp.tool()
async def get_weather_by_city(
    city: Annotated[str, Field(description="City name (e.g., 'London')")],
    country_code: Annotated[Optional[str], Field(description="Country code (e.g., 'uk' for United Kingdom)")] = None,
    units: Annotated[str, Field(description="Units of measurement: 'metric' (°C), 'imperial' (°F), or 'standard' (K)")] = "metric",
    lang: Annotated[str, Field(description="Language for weather descriptions (e.g., 'en', 'es', 'fr')")] = "en",
    ctx: Context = None
) -> str:
    """
    Get current weather information for a city.

    This tool fetches the current weather conditions for a specified city,
    optionally filtered by country code. You can specify the units of measurement
    and the language for weather descriptions.
    """
    return await weather_controller.get_weather_by_city(
        city=city,
        country_code=country_code,
        units=units,
        lang=lang,
        ctx=ctx
    )


@mcp.tool()
async def get_weather_by_coordinates(
    latitude: Annotated[float, Field(description="Latitude coordinate", ge=-90, le=90)],
    longitude: Annotated[float, Field(description="Longitude coordinate", ge=-180, le=180)],
    units: Annotated[str, Field(description="Units of measurement: 'metric' (°C), 'imperial' (°F), or 'standard' (K)")] = "metric",
    lang: Annotated[str, Field(description="Language for weather descriptions (e.g., 'en', 'es', 'fr')")] = "en",
    ctx: Context = None
) -> str:
    """
    Get current weather information for geographic coordinates.

    This tool fetches the current weather conditions for specified latitude and longitude
    coordinates. You can specify the units of measurement and the language for weather descriptions.
    """
    return await weather_controller.get_weather_by_coords(
        lat=latitude,
        lon=longitude,
        units=units,
        lang=lang,
        ctx=ctx
    )


@mcp.tool()
async def get_weather_by_zip(
    zip_code: Annotated[str, Field(description="Zip/postal code (e.g., '94040')")],
    country_code: Annotated[str, Field(description="Country code (e.g., 'us' for United States)")] = "us",
    units: Annotated[str, Field(description="Units of measurement: 'metric' (°C), 'imperial' (°F), or 'standard' (K)")] = "metric",
    lang: Annotated[str, Field(description="Language for weather descriptions (e.g., 'en', 'es', 'fr')")] = "en",
    ctx: Context = None
) -> str:
    """
    Get current weather information for a zip/postal code.

    This tool fetches the current weather conditions for a specified zip/postal code
    and country code. You can specify the units of measurement and the language for
    weather descriptions.
    """
    return await weather_controller.get_weather_by_zip(
        zip_code=zip_code,
        country_code=country_code,
        units=units,
        lang=lang,
        ctx=ctx
    )


@mcp.resource("weather://about")
def get_about_info() -> dict:
    """Provides information about the OpenWeatherMap MCP server."""
    return {
        "name": "OpenWeatherMap MCP Server",
        "version": "1.0.0",
        "description": "A server that provides tools to interact with the OpenWeatherMap API.",
        "capabilities": [
            "Current weather by city name",
            "Current weather by geographic coordinates",
            "Current weather by zip/postal code"
        ]
    }


def determine_transport():
    """
    Determine which transport to use based on environment or command line arguments.

    For Smithery deployment, we'll use stdio transport by default.
    For local development, we'll use HTTP transport by default.
    """
    # Check for environment variable
    transport_env = os.environ.get("MCP_TRANSPORT", "").lower()
    if transport_env in ["stdio", "streamable-http"]:
        return transport_env

    # Check for command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1].lower() == "stdio":
            return "stdio"
        elif sys.argv[1].lower() == "http":
            return "streamable-http"

    # Check if running in a container (likely Smithery)
    if os.environ.get("CONTAINER", "") or os.path.exists("/.dockerenv"):
        return "stdio"

    # Default to HTTP for local development
    return "streamable-http"


if __name__ == "__main__":
    transport = determine_transport()

    if transport == "stdio":
        # Run with stdio transport (for Smithery)
        mcp.run(transport="stdio")
    else:
        # Run with HTTP transport (for local development)
        mcp.run(
            transport="streamable-http",
            host="0.0.0.0",  # Listen on all interfaces
            port=int(os.environ.get("PORT", "8000")),
            path="/mcp",
            log_level="info"
        )
