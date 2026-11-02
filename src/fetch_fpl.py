import requests

url="https://fantasy.premierleague.com/api/bootstrap-static/"

def fetch_data():
    response = requests.get(url)
    data = response.json()
    return data

fixtures_url = "https://fantasy.premierleague.com/api/fixtures/"

def fetch_fixtures():
    fix_response = requests.get(fixtures_url)
    data_fix = fix_response.json()
    return data_fix

