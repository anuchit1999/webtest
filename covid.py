import requests
import json

url =requests.get("https://covid19.th-stat.com/api/open/today")

converd_covid_data = url.content.decode("utf-8")

coverd_obj = json.loads(converd_covid_data)

with open('covid.json','w') as json_file:
    data = json.dump(coverd_obj,json_file)
