"""
Controller for the OpenWeatherMap MCP server.
"""
from typing import Dict, Any, Optional
from fastmcp import Context

from provider import OpenWeatherMapProvider
from models import FormattedWeatherResponse, CurrentWeatherResponse


class WeatherController:
    """Controller for handling weather data requests."""
    
    def __init__(self):
        """Initialize the controller with the OpenWeatherMap provider."""
        self.provider = OpenWeatherMapProvider()
    
    async def get_weather_by_city(
        self, 
        city: str, 
        country_code: Optional[str] = None,
        units: str = "metric",
        lang: str = "en",
        ctx: Optional[Context] = None
    ) -> str:
        """
        Get current weather by city name.
        
        Args:
            city: City name
            country_code: Country code (ISO 3166)
            units: Units of measurement (standard, metric, imperial)
            lang: Language for weather descriptions
            ctx: MCP Context for logging
            
        Returns:
            Formatted weather information as string
        """
        if ctx:
            await ctx.info(f"Fetching weather for city: {city}")
            
        response, success = await self.provider.get_current_weather_by_city(
            city=city,
            country_code=country_code,
            units=units,
            lang=lang
        )
        
        if success:
            return self._format_weather_response(response, units)
        else:
            error_message = f"Error fetching weather data: {response.message}"
            if ctx:
                await ctx.error(error_message)
            return error_message
    
    async def get_weather_by_coords(
        self, 
        lat: float, 
        lon: float,
        units: str = "metric",
        lang: str = "en",
        ctx: Optional[Context] = None
    ) -> str:
        """
        Get current weather by geographic coordinates.
        
        Args:
            lat: Latitude
            lon: Longitude
            units: Units of measurement (standard, metric, imperial)
            lang: Language for weather descriptions
            ctx: MCP Context for logging
            
        Returns:
            Formatted weather information as string
        """
        if ctx:
            await ctx.info(f"Fetching weather for coordinates: {lat}, {lon}")
            
        response, success = await self.provider.get_current_weather_by_coords(
            lat=lat,
            lon=lon,
            units=units,
            lang=lang
        )
        
        if success:
            return self._format_weather_response(response, units)
        else:
            error_message = f"Error fetching weather data: {response.message}"
            if ctx:
                await ctx.error(error_message)
            return error_message
    
    async def get_weather_by_zip(
        self, 
        zip_code: str,
        country_code: str = "us",
        units: str = "metric",
        lang: str = "en",
        ctx: Optional[Context] = None
    ) -> str:
        """
        Get current weather by zip/postal code.
        
        Args:
            zip_code: Zip/postal code
            country_code: Country code (ISO 3166)
            units: Units of measurement (standard, metric, imperial)
            lang: Language for weather descriptions
            ctx: MCP Context for logging
            
        Returns:
            Formatted weather information as string
        """
        if ctx:
            await ctx.info(f"Fetching weather for zip code: {zip_code}, {country_code}")
            
        response, success = await self.provider.get_current_weather_by_zip(
            zip_code=zip_code,
            country_code=country_code,
            units=units,
            lang=lang
        )
        
        if success:
            return self._format_weather_response(response, units)
        else:
            error_message = f"Error fetching weather data: {response.message}"
            if ctx:
                await ctx.error(error_message)
            return error_message
    
    def _format_weather_response(self, weather: CurrentWeatherResponse, units: str) -> str:
        """
        Format the weather response into a human-readable string.
        
        Args:
            weather: Weather response from the provider
            units: Units of measurement used
            
        Returns:
            Formatted weather information as string
        """
        # Get the temperature unit symbol based on the units parameter
        temp_unit = "°C" if units == "metric" else "°F" if units == "imperial" else "K"
        
        # Get the wind speed unit based on the units parameter
        wind_unit = "m/s" if units == "metric" else "mph" if units == "imperial" else "m/s"
        
        # Get the main weather condition
        condition = weather.weather[0].description.capitalize() if weather.weather else "Unknown"
        
        # Format the response
        formatted = FormattedWeatherResponse(
            location=weather.name,
            country=weather.sys.country,
            temperature=weather.main.temp,
            feels_like=weather.main.feels_like,
            conditions=condition,
            humidity=weather.main.humidity,
            wind_speed=weather.wind.speed,
            wind_direction=weather.wind.deg,
            pressure=weather.main.pressure,
            visibility=weather.visibility / 1000,  # Convert to km
            sunrise=weather.sys.sunrise,
            sunset=weather.sys.sunset,
            timezone=weather.timezone
        )
        
        # Convert to a readable string
        return f"""
Weather for {formatted.location}, {formatted.country}:
Temperature: {formatted.temperature}{temp_unit} (Feels like: {formatted.feels_like}{temp_unit})
Conditions: {formatted.conditions}
Humidity: {formatted.humidity}%
Wind: {formatted.wind_speed} {wind_unit} at {formatted.wind_direction}°
Pressure: {formatted.pressure} hPa
Visibility: {formatted.visibility:.1f} km
        """.strip()
