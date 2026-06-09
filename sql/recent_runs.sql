SELECT 
    run_date,
    run_type,
    duration_minutes,
    distance_miles,
    ave_hr,
    max_hr,
    rpe,
    notes
FROM runs
WHERE user_id = :user_id
ORDER BY run_date 
DESC LIMIT :limit