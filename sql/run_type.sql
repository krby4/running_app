SELECT substr(run_date,1,7) AS month,
    run_type,
    count(run_type) as run_count,
    ROUND(SUM(distance_miles), 2) as total_miles,
    ROUND(SUM(duration_minutes) / 60, 2) as total_hours
FROM runs
WHERE user_id = :user_id
AND (:month is NULL or substr(run_date, 1, 7) = :month)
GROUP BY substr(run_date, 1, 7), run_type
ORDER BY run_count DESC;