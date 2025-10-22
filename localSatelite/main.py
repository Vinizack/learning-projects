import requests
from datetime import datetime

my_lat = -23.956288
my_lng = -46.326460

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()

data = response.json()

longitude = data["iss_position"]["longitude"]
atitude = data["iss_position"]["latitude"]

iss_postion = (longitude, latitude)

print(iss_postion)

parametros = {
    "lat": my_lat,
    "lng": my_lng,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parametros)
response.raise_for_status()
data = response.json()
sunrise = data["results"]["sunrise"]
sunset = data["results"]["sunset"]


print(sunrise)
print(sunset)

time_now = datetime.now()

print(time_now)







