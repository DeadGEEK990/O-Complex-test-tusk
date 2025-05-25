import requests
from datetime import date
from .errors import CityNotFoundError, WeatherFetchError


def get_coordinates(city_name):
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city_name, "count": 1}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if "results" in data and len(data["results"]) > 0:
            lat = data["results"][0]["latitude"]
            lon = data["results"][0]["longitude"]
            return lat, lon
    return None, None


def get_today_weather(lat, lon):
    url = "https://api.open-meteo.com/v1/forecast"
    today = date.today().isoformat()
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m",
        "start_date": today,
        "end_date": today,
        "timezone": "auto",
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    return None


def get_today_weather_by_city(city_name):
    lat, lon = get_coordinates(city_name)
    if lat and lon:
        weather = get_today_weather(lat, lon)
        if weather:
            return weather
        else:
            raise WeatherFetchError(
                "Не удалось получить прогноз погоды по данному городу!"
            )
    else:
        raise CityNotFoundError("Не удалось найти город!")
