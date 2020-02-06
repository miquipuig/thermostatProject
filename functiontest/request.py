import requests
import json
import numpy as np
url = 'https://api.openweathermap.org/data/2.5/weather?zip=08014,es&appid=35bef01f2be23b616aa0457916b79b5d'
data = '''{
  "query": {
    "bool": {
      "must": [
        {
          "text": {
            "record.document": "SOME_JOURNAL"
          }
        },
        {
          "text": {
            "record.articleTitle": "farmers"
          }
        }
      ],
      "must_not": [],
      "should": []
    }
  },
  "from": 0,
  "size": 50,
  "sort": [],
  "facets": {}
}'''
response = requests.get(url)
print(response.json())
print(response.text)
resp_dict=json.loads(response.text)
print(np.around(resp_dict['main']['temp']-273.15,decimals=1))
temp=np.around(resp_dict['main']['temp']-273.15,decimals=1)
temp_min=np.around(resp_dict['main']['temp_min']-273.15,decimals=1)
temp_max=np.around(resp_dict['main']['temp_max']-273.15,decimals=1)
humidity=np.around(resp_dict['main']['humidity']-273.15,decimals=2)
