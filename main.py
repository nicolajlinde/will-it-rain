import requests
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
ENDPOINT = os.getenv('ENDPOINT')
API_KEY = os.getenv('API_KEY')
LAT = os.getenv('LAT')
LON = os.getenv('LON')


weather_params = {
    "appid": API_KEY,
    "lat": LAT,
    "lon": LON,
    "exclude": "current,minutely,daily"
}

response = requests.get(ENDPOINT, params=weather_params)
response.raise_for_status()
data = response.json()

rain_total = ""
will_rain = False

for i in range(12):
    will_it_rain = data["hourly"][i]["weather"][0]

    if will_it_rain["id"] < 700:
        text = f"hallelujah, {will_it_rain['description']} in {i}H! Bring an umbrella."
        rain_total += text + "\n"
        will_rain = True

if will_rain:
    with smtplib.SMTP("smtp.gmail.com", 587) as conn:
        conn.starttls()
        conn.login(user=USER, password=PASSWORD)
        conn.sendmail(
            from_addr=USER,
            to_addrs="nicolajlpedersen@gmail.com",
            msg=f"Subject: IT RAINS!\n\nIt will rain at:\n\n{rain_total}"
        )
