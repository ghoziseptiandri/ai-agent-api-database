import urllib.parse
import urllib.request
import json


def get_weather(city: str):
    # 1. Convert city name into coordinates
    city_encoded = urllib.parse.quote(city)

    geocoding_url = (
        "https://geocoding-api.open-meteo.com/v1/search"
        f"?name={city_encoded}&count=1"
    )

    with urllib.request.urlopen(geocoding_url, timeout=10) as response:
        location_data = json.load(response)

    results = location_data.get("results")

    if not results:
        raise ValueError(f"City not found: {city}")

    location = results[0]

    latitude = location["latitude"]
    longitude = location["longitude"]

    # 2. Get current weather using the coordinates
    weather_url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}"
        f"&longitude={longitude}"
        "&current=temperature_2m,apparent_temperature,weather_code"
    )

    with urllib.request.urlopen(weather_url) as response:
        weather_data = json.load(response)

    current = weather_data["current"]

    return {
        "city": location["name"],
        "country": location.get("country"),
        "temperature": current["temperature_2m"],
        "apparent_temperature": current["apparent_temperature"],
        "weather_code": current["weather_code"],
    }