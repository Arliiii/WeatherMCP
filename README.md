# OpenWeatherMap MCP Server

A Model-Controller-Provider (MCP) server that integrates with the OpenWeatherMap API to provide weather data.

## Features

- Get current weather by city name
- Get current weather by geographic coordinates
- Get current weather by zip/postal code
- Support for different units of measurement (metric, imperial, standard)
- Support for multiple languages
- Smithery deployment support

## Architecture

This server follows the Model-Controller-Provider (MCP) architecture pattern:

- **Model**: Defines data structures for weather information
- **Controller**: Handles API requests and formats responses
- **Provider**: Interacts with the OpenWeatherMap API

## Setup

### Prerequisites

- Python 3.10 or higher
- OpenWeatherMap API key (get one at [OpenWeatherMap](https://openweathermap.org/api))

### Installation

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your OpenWeatherMap API key:
   ```
   OPENWEATHER_API_KEY=your_api_key_here
   ```

## Usage

### Running the Server Locally

Start the server with:

```bash
python server.py
```

By default, the server runs on `http://127.0.0.1:8000/mcp`.

You can also specify the transport mode:

```bash
# Run with HTTP transport (default)
python server.py http

# Run with stdio transport (for Smithery)
python server.py stdio
```

### Deploying with Smithery

This server includes configuration for deployment with Smithery:

1. Build the Docker image:
   ```bash
   docker build -t openweather-mcp .
   ```

2. Deploy to Smithery using the provided `smithery.yaml` configuration:
   ```bash
   smithery deploy
   ```

3. Configure your Smithery deployment with your OpenWeatherMap API key:
   ```json
   {
     "apiKey": "your_openweather_api_key_here",
     "units": "metric",
     "language": "en"
   }
   ```

### Connecting to the Server

You can connect to the server using any FastMCP client. For example:

```python
import asyncio
from fastmcp import Client

async def example():
    async with Client("http://127.0.0.1:8000/mcp") as client:
        # List available tools
        tools = await client.list_tools()
        print(f"Available tools: {tools}")

        # Get weather for a city
        result = await client.call_tool("get_weather_by_city", {"city": "London"})
        print(result[0].text)

if __name__ == "__main__":
    asyncio.run(example())
```

## Available Tools

### get_weather_by_city

Get current weather information for a city.

Parameters:
- `city` (string, required): City name (e.g., 'London')
- `country_code` (string, optional): Country code (e.g., 'uk' for United Kingdom)
- `units` (string, optional): Units of measurement ('metric', 'imperial', or 'standard')
- `lang` (string, optional): Language for weather descriptions (e.g., 'en', 'es', 'fr')

### get_weather_by_coordinates

Get current weather information for geographic coordinates.

Parameters:
- `latitude` (float, required): Latitude coordinate (-90 to 90)
- `longitude` (float, required): Longitude coordinate (-180 to 180)
- `units` (string, optional): Units of measurement ('metric', 'imperial', or 'standard')
- `lang` (string, optional): Language for weather descriptions (e.g., 'en', 'es', 'fr')

### get_weather_by_zip

Get current weather information for a zip/postal code.

Parameters:
- `zip_code` (string, required): Zip/postal code (e.g., '94040')
- `country_code` (string, optional): Country code (e.g., 'us' for United States)
- `units` (string, optional): Units of measurement ('metric', 'imperial', or 'standard')
- `lang` (string, optional): Language for weather descriptions (e.g., 'en', 'es', 'fr')

## Resources

### weather://about

Provides information about the OpenWeatherMap MCP server.

## License

MIT
