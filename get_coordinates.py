import configparser
from itertools import count
from urllib import request
import json

def get_api_key():
  config = configparser.ConfigParser()
  config.read('config.ini')
  return config['openweathermap']['api']

def get_coordinates(city_name, country_code = '', state = '',limit = 1):
  api_key = get_api_key()
  if country_code and state:
    api_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name},{state},{country_code}&limit={limit}&appid={api_key}"
  elif country_code and not state:
    api_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name},{country_code}&limit={limit}&appid={api_key}"
  else:
    api_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit={limit}&appid={api_key}"
  r = request.urlopen(api_url).read()
  list_of_data = json.loads(r)
  data = {}
  for item in list_of_data:
    if str(item["name"]) == city_name:
      if str(item["country"]) == "US":
        data = {
        "city": str(item['name']),
          "country_code": str(item['country']),
          "lon": str(item['lon']),
          "lat": str(item['lat']),
          "state": str(item['state'])
      }
      else:
        data = {
        "city": str(item['name']),
          "country_code": str(item['country']),
          "lon": str(item['lon']),
          "lat": str(item['lat']),
          "state": ''
        }
  return data

#print(get_coordinates("Kingston", "US", "MO"))