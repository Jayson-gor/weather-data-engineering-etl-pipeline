import requests
api_key = "934aed0eebc71a90147fb7b074b4ae01"
url = f"http://api.weatherstack.com/current?access_key={api_key}&query=Nairobi"

def fetch_data():
    print("Fetching weather data...")
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP errors
        print(f"Status Code: {response.status_code}")
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching API data: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    fetch_data()


def mock_fetch_data():
    return {
        "request": {
            "type": "City",
            "query": "Nairobi, Kenya",
            "language": "en",
            "unit": "m"
        },
        "location": {
            "name": "Nairobi",
            "country": "Kenya",
            "region": "Nairobi",
            "lat": "-1.286389",
            "lon": "36.817223",
            "timezone_id": "Africa/Nairobi",
            "localtime": "2025-08-22 11:30",
            "localtime_epoch": 1755858600,
            "utc_offset": "+3.0"
        },
        "current": {
            "observation_time": "08:30 AM",
            "temperature": 18,
            "weather_code": 116,
            "weather_icons": [
                "https://assets.weatherstack.com/images/wsymbols01_png_64/wsymbol_0002_sunny_intervals.png"
            ],
            "weather_descriptions": ["Partly cloudy"],
            "astro": {
                "sunrise": "06:33 AM",
                "sunset": "06:38 PM",
                "moonrise": "07:02 AM",
                "moonset": "07:15 PM",
                "moon_phase": "First Quarter",
                "moon_illumination": 55
            },
            "air_quality": {
                "co": "120.50",
                "no2": "28.005",
                "o3": "60",
                "so2": "6.2",
                "pm2_5": "7.45",
                "pm10": "8.12",
                "us-epa-index": "2",
                "gb-defra-index": "2"
            },
            "wind_speed": 5,
            "wind_degree": 90,
            "wind_dir": "E",
            "pressure": 1012,
            "precip": 0.2,
            "humidity": 78,
            "cloudcover": 35,
            "feelslike": 18,
            "uv_index": 6,
            "visibility": 10
        }
    }
