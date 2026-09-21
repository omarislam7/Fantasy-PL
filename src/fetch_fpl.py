import requests
import pandas as pd

url="https://fantasy.premierleague.com/api/bootstrap-static/"

response = requests.get(url)
print("Status Code:", response.status_code)
data = response.json()
print(data.keys())

