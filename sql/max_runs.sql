SELECT
    substr(run_date,1,:period) as period,
    run_date,
    run_type,
    ROUND(MAX(distance_miles),2) as max_distance,
    ROUND(MAX(duration_minutes),2) as max_duration
FROM runs
GROUP BY substr(run_date,1,:period)
ORDER BY period DESC;