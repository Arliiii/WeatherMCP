"""
Models for the OpenWeatherMap MCP server.
"""
from typing import List, Dict, Optional, Any, Union
from pydantic import BaseModel, Field


class Coordinates(BaseModel):
    """Geographic coordinates (latitude, longitude)."""
    lat: float = Field(description="Latitude")
    lon: float = Field(description="Longitude")


class WeatherCondition(BaseModel):
    """Weather condition information."""
    id: int = Field(description="Weather condition id")
    main: str = Field(description="Group of weather parameters (Rain, Snow, Clouds etc.)")
    description: str = Field(description="Weather condition within the group")
    icon: str = Field(description="Weather icon id")


class MainWeatherData(BaseModel):
    """Main weather metrics."""
    temp: float = Field(description="Temperature")
    feels_like: float = Field(description="Temperature accounting for human perception")
    temp_min: float = Field(description="Minimum temperature")
    temp_max: float = Field(description="Maximum temperature")
    pressure: int = Field(description="Atmospheric pressure (hPa)")
    humidity: int = Field(description="Humidity (%)")
    sea_level: Optional[int] = Field(None, description="Atmospheric pressure at sea level (hPa)")
    grnd_level: Optional[int] = Field(None, description="Atmospheric pressure at ground level (hPa)")


class Wind(BaseModel):
    """Wind information."""
    speed: float = Field(description="Wind speed")
    deg: int = Field(description="Wind direction (degrees)")
    gust: Optional[float] = Field(None, description="Wind gust speed")


class Clouds(BaseModel):
    """Cloud coverage information."""
    all: int = Field(description="Cloudiness (%)")


class Rain(BaseModel):
    """Rain volume information."""
    one_hour: Optional[float] = Field(None, alias="1h", description="Rain volume for last hour (mm)")
    three_hours: Optional[float] = Field(None, alias="3h", description="Rain volume for last 3 hours (mm)")


class Snow(BaseModel):
    """Snow volume information."""
    one_hour: Optional[float] = Field(None, alias="1h", description="Snow volume for last hour (mm)")
    three_hours: Optional[float] = Field(None, alias="3h", description="Snow volume for last 3 hours (mm)")


class SystemInfo(BaseModel):
    """System information from OpenWeatherMap."""
    type: Optional[int] = Field(None, description="Internal parameter")
    id: Optional[int] = Field(None, description="Internal parameter")
    country: str = Field(description="Country code")
    sunrise: int = Field(description="Sunrise time (unix, UTC)")
    sunset: int = Field(description="Sunset time (unix, UTC)")


class CurrentWeatherResponse(BaseModel):
    """Response model for current weather data."""
    coord: Coordinates = Field(description="Coordinates of the location")
    weather: List[WeatherCondition] = Field(description="Weather conditions")
    base: str = Field(description="Internal parameter")
    main: MainWeatherData = Field(description="Main weather metrics")
    visibility: int = Field(description="Visibility (meters)")
    wind: Wind = Field(description="Wind information")
    clouds: Clouds = Field(description="Cloud information")
    rain: Optional[Rain] = Field(None, description="Rain information")
    snow: Optional[Snow] = Field(None, description="Snow information")
    dt: int = Field(description="Time of data calculation (unix, UTC)")
    sys: SystemInfo = Field(description="System information")
    timezone: int = Field(description="Shift in seconds from UTC")
    id: int = Field(description="City ID")
    name: str = Field(description="City name")
    cod: int = Field(description="Internal parameter")


class WeatherError(BaseModel):
    """Error response from OpenWeatherMap API."""
    cod: Union[int, str] = Field(description="Error code")
    message: str = Field(description="Error message")


class FormattedWeatherResponse(BaseModel):
    """Formatted weather response for client consumption."""
    location: str = Field(description="Location name")
    country: str = Field(description="Country code")
    temperature: float = Field(description="Current temperature")
    feels_like: float = Field(description="Feels like temperature")
    conditions: str = Field(description="Weather conditions description")
    humidity: int = Field(description="Humidity percentage")
    wind_speed: float = Field(description="Wind speed")
    wind_direction: int = Field(description="Wind direction in degrees")
    pressure: int = Field(description="Atmospheric pressure (hPa)")
    visibility: float = Field(description="Visibility in kilometers")
    sunrise: int = Field(description="Sunrise time (unix, UTC)")
    sunset: int = Field(description="Sunset time (unix, UTC)")
    timezone: int = Field(description="Timezone offset from UTC in seconds")
