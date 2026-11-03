/*1] Who are the top 10 players by total FPL points this season? */
WITH player_points AS (
	SELECT p.first_name ||' '|| p.second_name AS player_name,
		SUM(ph.total_points) AS total_points
	FROM players p 
	JOIN player_history ph
		ON p.player_id = ph.player_id
	GROUP BY p.player_id
	ORDER BY total_points DESC
),
ranked_points AS(
	SELECT player_name,
		total_points,
		DENSE_RANK() OVER(ORDER BY total_points DESC) as player_rank
	FROM player_points
)

SELECT player_name,
	total_points,
	player_rank
FROM ranked_points 
WHERE player_rank <= 10;

/* 2] Which 10 players have the most attacking returns, where attacking returns = goals + assists? */
WITH attack_returns AS(
	SELECT p.first_name ||' '|| p.second_name AS player_name,
		SUM(ph.goals_scored + ph.assists) AS goal_contributions
	FROM players p
	JOIN player_history ph
		ON p.player_id = ph.player_id
	GROUP BY p.player_id
),
ranked_attack AS (
	SELECT *,
		RANK() OVER(ORDER BY goal_contributions DESC) AS attack_rank
	FROM attack_returns ar
)
SELECT *
FROM ranked_attack
WHERE attack_rank <= 10;

