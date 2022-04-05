import configparser
from urllib import request
import json

def get_api_key():
  config = configparser.ConfigParser()
  config.read('config.ini')
  return config['openweathermap']['api']

def get_weather_results(id):
  api_key = get_api_key()
  api_url = "https://api.openweathermap.org/data/2.5/weather?id={}&units=metric&appid={}".format(id, api_key)
  r = request.urlopen(api_url).read()
  list_of_data = json.loads(r)
  data = {
        "id": str(list_of_data['id']),
        "city": str(list_of_data['name']),
        "country_code": str(list_of_data['sys']['country']),
        "temp": str(list_of_data['main']['temp']) + 'C',
    }
  return data

#print(get_weather_results(420006353))