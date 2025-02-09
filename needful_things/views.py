import requests
from django.shortcuts import render
from django.views import View
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string


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


class MovieService:
    """Class to get top Sci-Fi movies from TMDb API"""

    @staticmethod
    def get_top_sci_fi_movies():
        """Gets TOP of Sci-Fi movies"""
        api_key = settings.MOVIE_DB_API_KEY
        url = f"https://api.themoviedb.org/3/discover/movie?api_key={api_key}&with_genres=878&sort_by=vote_average.desc&vote_count.gte=1000"

        try:
            response = requests.get(url).json()

            # API error handling
            if response.get("status_code"):
                print(f"API Error: {response.get('status_message')}")
                return []

            if "results" in response:
                movies = [
                    {
                        "title": movie.get("title", "Unknown Title"),
                        "year": movie.get("release_date", "N/A").split("-")[0] if movie.get("release_date") else "N/A",
                        "rating": movie.get("vote_average", "N/A"),
                        "description": movie.get("overview", "No description available."),
                        "poster": f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie.get(
                            "poster_path") else None
                    }
                    for movie in response.get("results", [])[:20]  # Get top 20 movies
                ]
                return movies
            else:
                print("No movie data found in API response.")
                return []

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return []


class RandomFactService:
    """Class for getting a random fact"""

    @staticmethod
    def get_random_fact():
        """Gets a random fact"""
        url = "https://uselessfacts.jsph.pl/random.json?language=en"
        try:
            response = requests.get(url).json()
            return response.get("text", "No fact available at the moment.")
        except requests.exceptions.RequestException:
            return "Failed to fetch a random fact."


class RandomFactView(View):
    """Returns a random fact via htmx"""

    def get(self, request):
        fact = RandomFactService.get_random_fact()
        html = render_to_string("needful_things/random_fact.html", {"random_fact": fact})
        return HttpResponse(html)


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

        # Get top Sci-Fi movies
        movies = MovieService.get_top_sci_fi_movies()

        # Get a random fact
        random_fact = RandomFactService.get_random_fact()

        return render(request, "needful_things/needful_things.html", {
            "weather": weather_data,
            "city": city,
            "country": country,
            "currencies": currencies,
            "result": None,
            "base_currency": "PLN",
            "target_currency": "EUR",
            "amount": 1.0,
            "movies": movies,
            "random_fact": random_fact
        })


class CurrencyConverterView(View):
    """Handles currency conversion via htmx"""

    def post(self, request):
        """Handles AJAX POST request from htmx"""
        base_currency = request.POST.get("base_currency", "PLN")
        target_currency = request.POST.get("target_currency", "EUR")
        amount = float(request.POST.get("amount", 1.0))

        result = CurrencyService.convert_currency(base_currency, target_currency, amount)

        html = render_to_string("needful_things/currency_result.html", {
            "result": result,
            "base_currency": base_currency,
            "target_currency": target_currency,
            "amount": amount
        })

        return HttpResponse(html)

