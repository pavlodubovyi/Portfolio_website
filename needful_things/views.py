import requests
from django.shortcuts import render
from django.conf import settings


def get_client_ip(request):
    """Get user's IP"""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def get_user_location(ip):
    """Determine user's location based on IP"""
    if ip == "127.0.0.1":
        return "Gdansk", "Poland"
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}").json()
        if response.get("status") != "success":
            return "Paris", "France"
        city = response.get("city")
        country = response.get("country")
        return city, country
    except requests.exceptions.RequestException:
        return "Rome", "Italy"


def get_weather(city):
    """Getting current weather data"""
    api_key = settings.OPENWEATHER_API_KEY
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url).json()

    if response.get("cod") != 200:
        return None

    return {
        "city": city,
        "temperature": response["main"]["temp"],
        "temp_min": response["main"]["temp_min"],
        "temp_max": response["main"]["temp_max"],
        "description": response["weather"][0]["description"].capitalize(),
        "icon": f"http://openweathermap.org/img/wn/{response['weather'][0]['icon']}@2x.png"
    }


def weather_view(request):
    """Main function to show weather"""
    ip = get_client_ip(request)
    city, country = get_user_location(ip)
    weather_data = get_weather(city)

    return render(request, "needful_things/needful_things.html", {
        "weather": weather_data,
        "city": city,
        "country": country
    })
