SELECT
    substr(run_date,1,4) AS year,
    COUNT(*) as run_count,
    ROUND(SUM(distance_miles), 2) as total_miles,
    ROUND(SUM(duration_minutes) / 60, 2) as total_hours,
    ROUND(AVG(distance_miles), 2) as ave_distance,
    ROUND(AVG(duration_minutes), 2) as ave_duration,
    ROUND(MAX(distance_miles), 2) as longest_distance_run,
    ROUND(MAX(duration_minutes), 2) as longest_time_run
FROM runs
WHERE (:year IS NULL OR substr(run_date, 1, 4) = :year)
GROUP BY substr(run_date,1,4)
ORDER BY year DESC;