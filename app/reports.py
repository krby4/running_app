from db import get_connection

def print_cursor_results(results):
    if results:
        headers = results[0].keys()
        print(" | ".join(headers))
        print("-" * 60)
        for row in results:
            print(" | ".join(str(row[h])for h in headers))
    else:
        print("No results found")

def run_query(query, params=()):
    conn = get_connection()
    results = conn.execute(query,params).fetchall()
    conn.close()
    return results

def recent_runs(limit):
    results = run_query("SELECT * FROM runs ORDER BY run_date DESC LIMIT ?",(limit,))
    print_cursor_results(results)

def longest_distance_runs(limit):
    results = run_query("SELECT * FROM runs ORDER BY distance_miles DESC LIMIT ?",(limit,))
    print_cursor_results(results)

def longest_duration_runs(limit):
    results = run_query("SELECT * FROM runs ORDER BY duration_minutes DESC LIMIT ?",(limit,))
    print_cursor_results(results)

# montly stats
def monthly_summary(month=None):
    results = run_query("""
    SELECT
        substr(run_date,1,7) AS month,
        COUNT(*) as run_count,
        ROUND(SUM(distance_miles), 2) as total_miles,
        ROUND(SUM(duration_minutes) / 60, 2) as total_hours,
        ROUND(AVG(distance_miles), 2) as ave_distance,
        ROUND(AVG(duration_minutes), 2) as ave_duration,
        ROUND(MAX(distance_miles), 2) as longest_distance_run,
        ROUND(MAX(duration_minutes), 2) as longest_time_run
    FROM runs
    WHERE (? IS NULL OR substr(run_date, 1, 7) = ?)
    GROUP BY substr(run_date,1,7)
    ORDER BY month DESC;
    """, (month,month))
    print_cursor_results(results)

def weekly_summary(week,month):
    results = run_query("""
    SELECT
        substr(run_date,1,7) AS month,
        COUNT(*) as run_count,
        ROUND(SUM(distance_miles), 2) as total_miles,
        ROUND(SUM(duration_minutes) / 60, 2) as total_hours,
        ROUND(AVG(distance_miles), 2) as ave_distance,
        ROUND(AVG(duration_minutes), 2) as ave_duration,
        ROUND(MAX(distance_miles), 2) as longest_distance_run,
        ROUND(MAX(duration_minutes), 2) as longest_time_run
    FROM runs
    WHERE (? IS NULL OR substr(run_date, 1, 7) = ?)
    GROUP BY substr(run_date,1,7)
    ORDER BY month DESC;
    """, (month,month))
    print_cursor_results(results)

def run_type(month=None):
    results = run_query("""
              SELECT substr(run_date,1,7) AS month,
              run_type,
              count(run_type) as run_count,
              ROUND(SUM(distance_miles), 2) as total_miles,
              ROUND(SUM(duration_minutes) / 60, 2) as total_hours
              FROM runs
              WHERE (? is NULL or substr(run_date, 1, 7) = ?)
              GROUP BY substr(run_date, 1, 7), run_type
              ORDER BY run_count DESC;
              """,(month,month))
    print_cursor_results(results)
    