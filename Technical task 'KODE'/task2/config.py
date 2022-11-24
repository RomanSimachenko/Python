import os

OPENWEATHER_API_URL = f"https://api.openweathermap.org/data/2.5/weather?q=%s&appid={os.getenv('API_KEY')}&units=metric"

LOCAL_REDIS_URL = "redis://127.0.0.1:6379"
