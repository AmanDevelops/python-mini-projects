import json
import os

import requests
from flask import Flask, redirect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from redis import Redis, exceptions

app = Flask(__name__)
r = Redis(
    host=os.environ.get("REDIS_HOST"),
    port=os.environ.get("REDIS_PORT"),
    decode_responses=True,
)

# Initialize rate limiter with Redis as storage
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    storage_uri=f"redis://{os.environ.get('REDIS_HOST')}:{os.environ.get('REDIS_PORT')}",
    default_limits=["1000 per day", "100 per hour"],
)

# Stops the server from booting up if there is a connection error
try:
    if r.ping():
        print("Succesfully Connected to Redis Server")
except exceptions.ConnectionError as e:
    print("Redis Connection", e)
    exit(1)


API_KEY = os.environ.get("WEATHER_API_KEY")
BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"


@app.route("/")
def home():
    return redirect("/weather/Lucknow")


@app.route("/weather/<string:city_name>")
@limiter.limit("1 per second")
def weather(city_name: str):
    # Get the Data from redis
    cache_weather_data = r.get(city_name)
    if cache_weather_data:
        return json.loads(cache_weather_data), 200

    # Get the data from API
    try:
        live_weather_request = requests.get(
            f"{BASE_URL}/{city_name}",
            params={
                "unitGroup": "us",
                "include": "current",
                "key": API_KEY,
                "contentType": "json",
            },
            timeout=5,
        )
    except requests.RequestException:
        return "Failed to fetch weather data", 502

    if live_weather_request.status_code == 400:
        return "Invalid Locaition", 400

    elif live_weather_request.status_code == 401:
        return "Invalid API Key", 400
    elif not live_weather_request.ok:
        return "Weather service unavailable", 503

    try:
        live_weather_data = live_weather_request.json()

        # Save the data to redis
        r.setex(city_name, 7200, json.dumps(live_weather_data))  # Cache for Two hours
        return live_weather_data, 200

    except requests.exceptions.JSONDecodeError:
        # API error
        return "Internal Server Error", 500
