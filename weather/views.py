from django.shortcuts import render, redirect
from .services.get_weather import get_today_weather_by_city
from .forms import GetWeatherForm
from django.http import HttpResponse, JsonResponse
from .services.errors import CityNotFoundError, WeatherFetchError
from django.contrib.auth.decorators import login_required
from .models import SearchHistory
import json


@login_required
def get_weather_view(request):
    if request.method == "POST":
        form = GetWeatherForm(request.POST)
        if form.is_valid():
            try:
                city = form.cleaned_data["city"]
                weather = get_today_weather_by_city(city)

                if request.user.is_authenticated:
                    SearchHistory.objects.create(user=request.user, query=city)

                hourly = weather.get("hourly", {})
                hourly_units = weather.get("hourly_units", {})

                times = hourly.get("time", [])
                keys = [k for k in hourly.keys() if k != "time"]

                parameters = []
                for key in keys:
                    label = key.replace("_", " ").title()
                    unit = hourly_units.get(key, "")
                    parameters.append({"key": key, "label": label, "unit": unit})

                hourly_data = []
                for i, time_str in enumerate(times):
                    row = [time_str]
                    for param in parameters:
                        values = hourly.get(param["key"], [])
                        row.append(values[i] if i < len(values) else None)
                    hourly_data.append(row)

                context = {
                    "city": city,
                    "timezone": weather.get("timezone", ""),
                    "parameters": parameters,
                    "hourly_data": hourly_data,
                }
                response = render(request, "weather/display_weather.html", context)
                response.set_cookie("last_query", city)
                return response
            except CityNotFoundError as e:
                return JsonResponse({"error": str(e)}, status=404)
            except WeatherFetchError as e:
                return JsonResponse({"error": str(e)}, status=500)
    else:
        form = GetWeatherForm()
        last_query = request.COOKIES.get("last_query")
        form = GetWeatherForm(initial={"city": last_query} if last_query else None)
    return render(request, "weather/get_weather.html", {"form": form})
