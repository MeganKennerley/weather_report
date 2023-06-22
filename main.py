import requests
from datetime import datetime
import os
from twilio.rest import Client

api_key = os.environ.get("WEATHER_API_KEY")
url = "https://api.openweathermap.org/data/2.5/forecast"

params = {
    "lat": float(os.environ.get("LAT")),
    "lon": float(os.environ.get("LON")),
    "appid": api_key,
    "units": "metric"
}

response = requests.get(url, params=params)
response.raise_for_status()
weather_data = response.json()

account_sid = os.environ.get("account_sid")
auth_token = os.environ.get("SMS_AUTH_TOKEN")
client = Client(account_sid, auth_token)

days = {}

for date in weather_data["list"]:

    current_day = datetime.utcfromtimestamp(date["dt"]).strftime('%A')
    current_temp = round(int(date['main']['temp']))

    if current_day not in days:
        days[current_day] = current_temp

    else:
        days[current_day] = max([current_temp, days[current_day]])

    main_date = datetime.utcfromtimestamp(date["dt"]).strftime('%d')
    main_hour = datetime.utcfromtimestamp(date["dt"]).strftime('%H')
    if int(date["weather"][0]["id"]) < 700 and main_date == datetime.today().day:
        message = client.messages \
                        .create(
                            body=f"Weekly forcast:\nYou will need an Umbrella today at {main_hour}:00 ☔️",
                            from_=SMS_NUMBER,
                            to=TO_NUMBER
        )

my_message = ""
for day in days:
    my_message += f"{day} - {days[day]}°C\n"


message = client.messages \
                .create(
                    body=f"Weekly forcast☀️:\n{my_message}",
                    from_=SMS_NUMBER,
                    to=TO_NUMBER
                 )

