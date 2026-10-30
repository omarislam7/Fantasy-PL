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

cursor.execute("DELETE FROM positions;") ##TEMPPPP

for _,row in positions_df.iterrows():
    cursor.execute(
        """
        INSERT INTO positions (position_id, singular_name, singular_name_short, squad_select, squad_min_play, squad_max_play)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (row["position_id"], row["singular_name"], row["singular_name_short"], row["squad_select"], row["squad_min_play"], row["squad_max_play"])
    )
conn.commit()
cursor.close()
conn.close()