from __future__ import annotations

from fastmcp import FastMCP

# Create the server
mcp = FastMCP("weather-tools")

# Replace with a real API later if you want.
def _simple_weather_for_city(city: str) -> dict:
    c = city.strip()
    if not c:
        raise ValueError("city must be a non-empty string")

    key = c.lower()

    # A couple of friendly canned examples
    presets = {
        "vancouver": {"condition": "Rain", "temp_c": 7, "wind_kph": 18},
        "toronto": {"condition": "Cloudy", "temp_c": -2, "wind_kph": 22},
        "calgary": {"condition": "Clear", "temp_c": -10, "wind_kph": 12},
        "montreal": {"condition": "Snow", "temp_c": -6, "wind_kph": 25},
    }
    if key in presets:
        return {"city": c.title(), **presets[key]}

    # default if no match.
    temp_c = 27      # -10 .. 24
    wind_kph = 2     # 1 .. 40
    condition = "Sunny"
    return {"city": c.title(), "condition":
            condition, "temp_c": temp_c, "wind_kph": wind_kph}

@mcp.tool()
def get_weather(city: str) -> dict:
    return _simple_weather_for_city(city)

@mcp.tool()
def get_fahrenheitFromCelsius(temp: float) -> float:
    return temp * 1.8 + 32

if __name__ == "__main__":
    # STDIO transport by default (best for local labs and desktop MCP clients)
    mcp.run()
