import requests

url="https://fantasy.premierleague.com/api/bootstrap-static/"

def fetch_data():
    response = requests.get(url)
    data = response.json()
    return data
