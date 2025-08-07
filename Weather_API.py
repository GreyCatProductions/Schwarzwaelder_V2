import requests


def get_weather(city_name):
    api_key = '2b0575fe496d5e8c7c4c0cf5b80fd8cf'
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        weather_id = data['weather'][0]['id']
        temperature = data['main']['temp']

        # Weather condition
        if weather_id >= 200 and weather_id < 300:
            weather = "Sturm"  # Thunderstorm
        elif weather_id >= 300 and weather_id < 400:
            weather = "Regen"  # Drizzle
        elif weather_id >= 500 and weather_id < 600:
            weather = "Regen"  # Rain
        elif weather_id >= 600 and weather_id < 700:
            weather = "Schneefall"  # Snow
        elif weather_id >= 700 and weather_id < 800:
            weather = "Nebel"  # Fog
        elif weather_id == 800:
            weather = "Sonnig (Tag)"  # Clear sky
        else:
            weather = "Wolkig"  # Cloudy

        return round(temperature, 0), weather
    else:
        return None, None
