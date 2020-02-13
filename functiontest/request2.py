import requests
import json
import numpy as np
url = 'https://api.openweathermap.org/data/2.5/weather?zip=08014,es&appid=35bef01f2be23b616aa0457916b79b5d&lang=ca'
response = requests.get(url)
print(response.json())
resp_dict=json.loads(response.text)
print(np.around(resp_dict['main']['temp']-273.15,decimals=1))
weatherTemp=np.around(resp_dict['main']['temp']-273.15,decimals=1)
weatherTemp_min=np.around(resp_dict['main']['temp_min']-273.15,decimals=1)
weatherTemp_max=np.around(resp_dict['main']['temp_max']-273.15,decimals=1)
weatherHumidity=np.around(resp_dict['main']['humidity']-273.15,decimals=2)
weatherIcon=json.loads(json.dumps(resp_dict['weather'][0]))['icon']
weatherDesciption=json.loads(json.dumps(resp_dict['weather'][0]))['description']

print(weatherDesciption)