from fetch_fpl import fetch_data
import pandas as pd
from connect import connection

data = fetch_data() ## get the data from API, then clean

teams_df = pd.DataFrame(data["teams"])
teams_df = teams_df[["id", "code", "short_name", "name"]]

teams_df = teams_df.rename(columns=
                           {'id': 'team_id'})
print(teams_df.head())

conn = connection() ##create the connection

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
conn.commit()
cursor.close()
conn.close()