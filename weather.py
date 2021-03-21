import requests
import json

# This function will get a Rest_Api from me and will create a dictionary which will contain all of the weather information in the zip code
def weather_api(zip):
    api_key="224c355caba19df860436dcec3409f31"
    url="https://api.openweathermap.org/data/2.5/weather?zip=%s&units=imperial&appid=%s" % (zip,api_key)
    response=requests.get(url)
    data = json.loads(response.text)
    return(data)

