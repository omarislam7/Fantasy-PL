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
    kickoff_time TIMESTAMPTZ
    home_team INT NOT NULL,
    home_team_score INT,
    away_team INT NOT NULL,
    away_team_score INT,
    code INT UNIQUE NOT NULL,
    event INT NOT NULL,

    FOREIGN KEY (event) REFERENCES gameweek(gameweek_id),
    FOREIGN KEY (home_team) REFERENCES teams(team_id),
    FOREIGN KEY (home_team) REFERENCES teams(team_id)
);


