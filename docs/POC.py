import requests
import json
api_key="224c355caba19df860436dcec3409f31"
lon="-122.0469"
lat="37.5735"
zip='94555'
url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric" % (lat, lon, api_key)
response=requests.get(url)
data = json.loads(response.text)
print(data)