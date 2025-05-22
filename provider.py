"""
Provider for the OpenWeatherMap API.
"""
import os
import httpx
from typing import Dict, Any, Optional, Union, Tuple
from dotenv import load_dotenv

from models import CurrentWeatherResponse, WeatherError

# Load environment variables
load_dotenv()

class OpenWeatherMapProvider:
    """Provider for interacting with the OpenWeatherMap API."""
    
    BASE_URL = "https://api.openweathermap.org/data/2.5"
    
    def __init__(self):
        """Initialize the provider with API key from environment variables."""
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        if not self.api_key:
            raise ValueError("OpenWeatherMap API key not found. Please set OPENWEATHER_API_KEY environment variable.")
        
        self.headers = {
            "User-Agent": "OpenWeatherMapMCPServer/1.0",
            "Accept": "application/json"
        }
    
    async def get_current_weather_by_coords(
        self, 
        lat: float, 
        lon: float, 
        units: str = "metric",
        lang: str = "en"
    ) -> Tuple[Union[CurrentWeatherResponse, WeatherError], bool]:
        """
        Get current weather by geographic coordinates.
        
        Args:
            lat: Latitude
            lon: Longitude
            units: Units of measurement (standard, metric, imperial)
            lang: Language for weather descriptions
            
        Returns:
            Tuple containing the response (either weather data or error) and a boolean indicating success
        """
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
            "units": units,
            "lang": lang
        }
        
        return await self._make_request("/weather", params)
    
    async def get_current_weather_by_city(
        self, 
        city: str, 
        country_code: Optional[str] = None,
        units: str = "metric",
        lang: str = "en"
    ) -> Tuple[Union[CurrentWeatherResponse, WeatherError], bool]:
        """
        Get current weather by city name.
        
        Args:
            city: City name
            country_code: Country code (ISO 3166)
            units: Units of measurement (standard, metric, imperial)
            lang: Language for weather descriptions
            
        Returns:
            Tuple containing the response (either weather data or error) and a boolean indicating success
        """
        location = city
        if country_code:
            location = f"{city},{country_code}"
            
        params = {
            "q": location,
            "appid": self.api_key,
            "units": units,
            "lang": lang
        }
        
        return await self._make_request("/weather", params)
    
    async def get_current_weather_by_zip(
        self, 
        zip_code: str, 
        country_code: str = "us",
        units: str = "metric",
        lang: str = "en"
    ) -> Tuple[Union[CurrentWeatherResponse, WeatherError], bool]:
        """
        Get current weather by zip/postal code.
        
        Args:
            zip_code: Zip/postal code
            country_code: Country code (ISO 3166)
            units: Units of measurement (standard, metric, imperial)
            lang: Language for weather descriptions
            
        Returns:
            Tuple containing the response (either weather data or error) and a boolean indicating success
        """
        params = {
            "zip": f"{zip_code},{country_code}",
            "appid": self.api_key,
            "units": units,
            "lang": lang
        }
        
        return await self._make_request("/weather", params)
    
    async def _make_request(
        self, 
        endpoint: str, 
        params: Dict[str, Any]
    ) -> Tuple[Union[CurrentWeatherResponse, WeatherError], bool]:
        """
        Make a request to the OpenWeatherMap API.
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            
        Returns:
            Tuple containing the response (either weather data or error) and a boolean indicating success
        """
        url = f"{self.BASE_URL}{endpoint}"
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params, headers=self.headers, timeout=30.0)
                data = response.json()
                
                if response.status_code == 200:
                    return CurrentWeatherResponse(**data), True
                else:
                    return WeatherError(**data), False
                    
        except httpx.RequestError as e:
            return WeatherError(cod=500, message=f"Request error: {str(e)}"), False
        except Exception as e:
            return WeatherError(cod=500, message=f"Unexpected error: {str(e)}"), False
