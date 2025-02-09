import requests
from django.shortcuts import render
from django.views import View
from django.conf import settings


class WeatherService:
    """Class for managing weather widget"""

    @staticmethod
    def get_user_ip(request):
        """Gets user IP address"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip

    @staticmethod
    def get_user_location(ip):
        """Gets user ip and location"""
        if ip == "127.0.0.1":
            return "Gdansk", "Poland"
        try:
            response = requests.get(f"http://ip-api.com/json/{ip}").json()
            if response.get("status") != "success":
                return "Paris", "France"
            return response.get("city"), response.get("country")
        except requests.exceptions.RequestException:
            return "Rome", "Italy"

    @staticmethod
    def get_weather(city):
        """Gets current weather"""
        api_key = settings.OPENWEATHER_API_KEY
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        try:
            response = requests.get(url).json()
            if int(response.get("cod", 0)) != 200:
                return None
            return {
                "city": city,
                "temperature": response["main"]["temp"],
                "temp_min": response["main"]["temp_min"],
                "temp_max": response["main"]["temp_max"],
                "description": response["weather"][0]["description"].capitalize(),
                "icon": f"https://openweathermap.org/img/wn/{response['weather'][0]['icon']}@2x.png"
            }
        except requests.exceptions.RequestException:
            return None


class CurrencyService:
    """Currency exchange class"""

    @staticmethod
    def get_available_currencies():
        """Gets available currencies"""
        api_key = settings.EXCHANGE_RATES_API_KEY
        url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/USD"

        try:
            response = requests.get(url).json()
            if "conversion_rates" in response:
                return list(response["conversion_rates"].keys())  # List of all currencies
            print("API Error:", response)
            return ["USD", "EUR", "GBP", "PLN", "UAH"]  # Default list if API fails
        except requests.exceptions.RequestException:
            return ["USD", "EUR", "GBP", "PLN", "UAH"]

    @staticmethod
    def convert_currency(base_currency, target_currency, amount):
        """Converts currency"""
        api_key = settings.EXCHANGE_RATES_API_KEY
        url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{base_currency}/{target_currency}/{amount}"

        try:
            response = requests.get(url).json()
            if "conversion_rate" in response:
                return float(amount) * float(response["conversion_rate"])
            print("API Error:", response)
            return None
        except requests.exceptions.RequestException:
            return None


class NeedfulThingsView(View):
    """Main page view, handling other widgets"""

    def get(self, request):
        """Handles GET request to load the page"""

        # Get weather
        ip = WeatherService.get_user_ip(request)
        city, country = WeatherService.get_user_location(ip)
        weather_data = WeatherService.get_weather(city)

        # Get available currencies
        currencies = CurrencyService.get_available_currencies()

        return render(request, "needful_things/needful_things.html", {
            "weather": weather_data,
            "city": city,
            "country": country,
            "currencies": currencies,
            "result": None,
            "base_currency": "PLN",
            "target_currency": "EUR",
            "amount": 1.0
        })

    def post(self, request):
        """Handles currency conversion inside the same widget"""

        base_currency = request.POST.get("base_currency", "PLN")
        target_currency = request.POST.get("target_currency", "EUR")
        amount = float(request.POST.get("amount", 1.0))

        result = CurrencyService.convert_currency(base_currency, target_currency, amount)
        currencies = CurrencyService.get_available_currencies()

        ip = WeatherService.get_user_ip(request)
        city, country = WeatherService.get_user_location(ip)
        weather_data = WeatherService.get_weather(city)

        return render(request, "needful_things/needful_things.html", {
            "weather": weather_data,
            "city": city,
            "country": country,
            "currencies": currencies,
            "result": result,
            "base_currency": base_currency,
            "target_currency": target_currency,
            "amount": amount
        })
