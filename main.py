import requests
import smtplib

USER = "nicowishesyouahappybirthday@gmail.com"
PASSWORD = "xmebpypmfzhilrnk"
ENDPOINT = "https://api.openweathermap.org/data/2.5/onecall"
API_KEY = "37ff893b831e3986eb1092909ee0ebde"
LAT = "56.162937"
LON = "10.203921"

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

# will_rain = False
# will_it_rain = data["hourly"][:11]
# for x in will_it_rain:
#     if x["weather"][0]["id"] < 700:
#         will_rain = True
#
# if will_rain:
#     print(f"hallelujah, it will rain! Bring an umbrella.")