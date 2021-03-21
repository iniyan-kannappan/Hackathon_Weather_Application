import requests
import json

def weather_api(zip):
    api_key="224c355caba19df860436dcec3409f31"
    url="https://api.openweathermap.org/data/2.5/weather?zip=%s&units=imperial&appid=%s" % (zip,api_key)
    response=requests.get(url)
    data = json.loads(response.text)
    return(data)

