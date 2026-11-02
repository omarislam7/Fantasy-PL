from fetch_fpl import fetch_data
from fetch_fpl import fetch_fixtures
from fetch_fpl import fetch_players
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

cursor.execute("DELETE FROM player_history;")
cursor.execute("DELETE FROM history_past;")
cursor.execute("DELETE FROM fixtures;") ##TEMPPP
cursor.execute("DELETE FROM players;") ##TEMPPP
cursor.execute("DELETE FROM positions;") ##TEMPPPP
cursor.execute("DELETE FROM gameweek;")
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


##Gameweek data
gameweek_df = pd.DataFrame(data["events"])
gameweek_df = gameweek_df[["id", "name", "deadline_time"]]
gameweek_df = gameweek_df.rename(columns=
                                 {"id": "gameweek_id"})

for _,row in gameweek_df.iterrows():
    cursor.execute(
        """
        INSERT INTO gameweek (gameweek_id, name, deadline_time)
        VALUES (%s, %s, %s)
        """,
        (row["gameweek_id"], row["name"], row["deadline_time"])
    )

#Fixture tables insert
fixture_data = fetch_fixtures()
fixtures_df = pd.DataFrame(fixture_data)

fixtures_df = fixtures_df[["id","kickoff_time", "team_h", "team_h_score","team_a", "team_a_score", "code", "event"]]
fixtures_df = fixtures_df.rename(columns=
                                   {"id": "fixture_id",
                                    "team_h":"home_team_id",
                                    "team_h_score": "home_team_score",
                                    "team_a": "away_team_id",
                                    "team_a_score": "away_team_score"
                                   })

nullable_cols = ["kickoff_time", "home_team_score" , "away_team_score"]

for col in nullable_cols:
    fixtures_df[col] = fixtures_df[col].astype(object)
    fixtures_df.loc[fixtures_df[col].isna(), col] = None

for _,row in fixtures_df.iterrows():
    cursor.execute(
        """
        INSERT INTO fixtures (fixture_id, kickoff_time, home_team_id, home_team_score, away_team_id, away_team_score, code, event)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """,
        (row["fixture_id"], row["kickoff_time"], row["home_team_id"], row["home_team_score"], row["away_team_id"], row["away_team_score"], row["code"], row["event"])
    )

#player history table insert
players_df = players_df.sort_values("player_id") ##SORT PLAYER_ID SO IT INSERTED IN ORDER

for player in players_df["player_id"]:
        
    ##PLAYER_HISTORY TABLE
    player_data = fetch_players(player)
    player_history_df = pd.DataFrame(player_data["history"])

    if not player_history_df.empty:
        player_history_df = player_history_df[['element', 'fixture', 'opponent_team', 'total_points', 'was_home', 'kickoff_time', 'round', 'minutes', 'goals_scored', 
                                            'assists', 'clean_sheets', 'goals_conceded', 'own_goals', 'penalties_saved', 'penalties_missed', 'yellow_cards','red_cards',
                                                'saves', 'bonus', 'bps', 'influence', 'creativity', 'threat', 'ict_index', 'clearances_blocks_interceptions', 'recoveries',
                                                'tackles', 'defensive_contribution', 'starts', 'expected_goals', 'expected_assists', 'expected_goal_involvements',
                                                'expected_goals_conceded', 'value', 'transfers_balance', 'selected','transfers_in', 'transfers_out']]
        
        player_history_df = player_history_df.rename(columns=
                                                    {"element": "player_id",
                                                    "fixture": "fixture_id",
                                                    "opponent_team": "opponent_team_id",
                                                    "round": "gameweek_id"
                                                    })

        columns = list(player_history_df.columns)
        column_names = ", ".join(columns)

        placeholders = ", ".join(["%s"] * len(columns))
        for _,row in player_history_df.iterrows():
            cursor.execute(
                f"""
                INSERT INTO player_history ({column_names})
                VALUES ({placeholders})
                """, 
                tuple(row[col] for col in columns)
            )

        print(f"Finished Loading player_history table for: {player}") #JUST A CHECK

    ##HISTORY_PAST TABLE INSERTION
    player_past_history_df =  pd.DataFrame(player_data["history_past"]) ## NO NEED TO RENAME OR EVEN CHOOSE ANY COLUMNS, USE ALL OF THE COLUMNS
    
    if not player_past_history_df.empty:
        print(f"Loading history_past table for player_id: {player}") #JUST A CHECK

        columns_past = list(player_past_history_df.columns)
        columns_past_names = ", ".join(columns_past)
        placeholders_past = ", ".join(["%s"] * len(columns_past))

        for _,row in player_past_history_df.iterrows():
            cursor.execute(
                f"""
                INSERT INTO history_past({columns_past_names})
                VALUES ({placeholders_past})
                """,
                tuple(row[col] for col in columns_past)
            )

conn.commit()
cursor.close()
conn.close()