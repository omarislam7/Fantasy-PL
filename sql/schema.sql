CREATE TABLE teams(
    team_id int PRIMARY KEY,
    code int UNIQUE NOT NULL,
    short_name varchar(3) NOT NULL,
    name varchar(100) NOT NULL
);

CREATE TABLE positions(
    position_id int PRIMARY KEY,
    singular_name varchar(50) UNIQUE NOT NULL,
    singular_name_short varchar(5) UNIQUE NOT NULL,
    squad_select int NOT NULL,
    squad_min_play int NOT NULL,
    squad_max_play int NOT NULL
);

CREATE TABLE players(
    player_id int PRIMARY KEY,
    code int UNIQUE NOT NULL,
    first_name varchar(100) NOT NULL,
    second_name varchar(100) NOT NULL,
    web_name varchar(100) NOT NULL,
    team_id int NOT NULL,
    position_id int NOT NULL,
    photo TEXT,
    birth_date DATE NOT NULL,

    FOREIGN KEY (team_id) REFERENCES teams(team_id),
    FOREIGN KEY (position_id) REFERENCES positions(position_id)
);

CREATE TABLE gameweek(
    gameweek_id int PRIMARY KEY,
    name TEXT NOT NULL,
    deadline_time TIMESTAMPTZ NOT NULL
);

CREATE TABLE fixtures(
    fixture_id INT PRIMARY KEY,
    kickoff_time TIMESTAMPTZ,
    home_team INT NOT NULL,
    home_team_score INT,
    away_team INT NOT NULL,
    away_team_score INT,
    code INT UNIQUE NOT NULL,
    event INT NOT NULL,

    FOREIGN KEY (event) REFERENCES gameweek(gameweek_id),
    FOREIGN KEY (home_team) REFERENCES teams(team_id),
    FOREIGN KEY (away_team) REFERENCES teams(team_id)
);

CREATE TABLE player_history (
    -- identifiers
    player_id INT NOT NULL,
    fixture_id INT NOT NULL,
    opponent_team_id INT,
    gameweek_id INT NOT NULL,
    was_home BOOLEAN NOT NULL,
    kickoff_time TIMESTAMPTZ NOT NULL,
    
    -- performance
    total_points INT NOT NULL,
    minutes INT NOT NULL,
    goals_scored INT NOT NULL,
    assists INT NOT NULL,
    clean_sheets INT NOT NULL,
    goals_conceded INT NOT NULL,
    own_goals INT NOT NULL,

    -- discipline/goalkeeping/bonus
    penalties_saved INT NOT NULL,
    penalties_missed INT NOT NULL,
    yellow_cards INT NOT NULL,
    red_cards INT NOT NULL,
    saves INT NOT NULL,
    bonus INT NOT NULL,
    bps INT NOT NULL,

    -- FPL performance and metrics
    influence NUMERIC NOT NULL,
    creativity NUMERIC NOT NULL,
    threat NUMERIC NOT NULL,
    ict_index NUMERIC NOT NULL,

    clearances_blocks_interceptions INT NOT NULL,
    recoveries INT NOT NULL,
    tackles INT NOT NULL,
    defensive_contribution INT NOT NULL,
    starts INT NOT NULL,

    --expected stats
    expected_goals NUMERIC NOT NULL,
    expected_assists NUMERIC NOT NULL,
    expected_goal_involvements NUMERIC NOT NULL,
    expected_goals_conceded NUMERIC NOT NULL,

    --market/ownership
    value INT NOT NULL,
    transfers_balance INT NOT NULL,
    selected INT NOT NULL,
    transfers_in INT NOT NULL,
    transfers_out INT NOT NULL,
    
    PRIMARY KEY (player_id, fixture_id),

    FOREIGN KEY (player_id) REFERENCES players(player_id),
    FOREIGN KEY (fixture_id) REFERENCES fixtures(fixture_id),
    FOREIGN KEY (opponent_team_id) REFERENCES teams(team_id),
    FOREIGN KEY (gameweek_id) REFERENCES gameweek(gameweek_id)
);

