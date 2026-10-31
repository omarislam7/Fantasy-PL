from fetch_fpl import fetch_data
import pandas as pd
from connect import connection

data = fetch_data() ## get the data from API, then clean

# Load TEAM table
teams_df = pd.DataFrame(data["teams"])
teams_df = teams_df[["id", "code", "short_name", "name"]]
teams_df = teams_df.rename(columns=
                           {'id': 'team_id'})
print(teams_df.head())

conn = connection() #create the connection
cursor = conn.cursor()

cursor.execute("DELETE FROM players;") ##TEMPPP
cursor.execute("DELETE FROM positions;") ##TEMPPPP
cursor.execute("DELETE FROM teams;") ##TEMPORARYYY for testing

for _, row in teams_df.iterrows():
    cursor.execute(
        """
        INSERT INTO teams (team_id, code, short_name, name)
        VALUES (%s, %s, %s, %s)
        """,
        (row["team_id"], row["code"], row["short_name"], row["name"])
    )

# Load Position Table
positions_df = pd.DataFrame(data["element_types"])
positions_df = positions_df[["id", "singular_name", "singular_name_short", "squad_select", "squad_min_play","squad_max_play"]]
positions_df = positions_df.rename(columns=
                                   {"id": "position_id"})
print(positions_df.head(3))

for _,row in positions_df.iterrows():
    cursor.execute(
        """
        INSERT INTO positions (position_id, singular_name, singular_name_short, squad_select, squad_min_play, squad_max_play)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (row["position_id"], row["singular_name"], row["singular_name_short"], row["squad_select"], row["squad_min_play"], row["squad_max_play"])
    )

#LOAD players table
players_df = pd.DataFrame(data["elements"])
players_df = players_df[["id", "first_name", "second_name", "team", "element_type", "photo", "birth_date", "code", "web_name"]]
players_df = players_df.rename(columns=
                               {"id": "player_id",
                                "team": "team_id",
                                "element_type": "position_id"})
print(players_df.head(6))

players_df["birth_date"] = players_df["birth_date"].astype(object)
players_df.loc[players_df["birth_date"].isna(), "birth_date"] = None


for _,row in players_df.iterrows():
    cursor.execute(
        """
        INSERT INTO players (player_id, first_name, second_name, team_id, position_id, photo, birth_date, code, web_name)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (row["player_id"], row["first_name"], row["second_name"], row["team_id"], row["position_id"], row["photo"], row["birth_date"], row["code"], row["web_name"])
    )



conn.commit()
cursor.close()
conn.close()