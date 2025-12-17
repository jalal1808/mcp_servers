import os
import httpx
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("WeatherService")
API_KEY = os.getenv("WEATHER_API_KEY")

@mcp.tool()
async def get_weather(city: str) -> str:
    """Fetches real-time weather for a given city name."""
    if not API_KEY:
        return "Error: WEATHER_API_KEY not set."

    url = "http://api.weatherapi.com/v1/current.json"
    params = {
        "key": API_KEY,
        "q": city,
        "aqi": "no"
    }

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params)

        if resp.status_code != 200:
            return f"Error fetching weather: {resp.text}"

        data = resp.json()

        temp = data["current"]["temp_c"]
        desc = data["current"]["condition"]["text"]

        return f"The current weather in {city} is {temp}°C with {desc}."

if __name__ == "__main__":
    mcp.run()
