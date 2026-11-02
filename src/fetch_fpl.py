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

def fetch_players(player_id):
    player_url = f"https://fantasy.premierleague.com/api/element-summary/{player_id}/"
    player_response = requests.get(player_url)
    player_data = player_response.json()
    return player_data
