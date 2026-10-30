import requests
import pandas as pd

url="https://fantasy.premierleague.com/api/bootstrap-static/"

def fetch_data():
    response = requests.get(url)
    data = response.json()
    return data
