from db import get_connection
import pathlib

def print_cursor_results(results):
    if results:
        headers = results[0].keys()
        print(" | ".join(headers))
        print("-" * 60)
        for row in results:
            print(" | ".join(str(row[h])for h in headers))
    else:
        print("No results found")

def load_query(filename):
    base_dir = pathlib.Path(__file__).resolve().parent
    project_dir = base_dir.parent
    sql_dir = project_dir / "sql"
    return pathlib.Path(sql_dir / filename).read_text(encoding="utf-8")

def run_query(query, params=()):
    conn = get_connection()
    results = conn.execute(query,params).fetchall()
    conn.close()
    return results

def recent_runs(user_id,limit=10):
    query = load_query("recent_runs.sql")
    return run_query(query,(user_id,limit)) 
    # print_cursor_results(results)

def longest_distance_runs(limit):
    return run_query("SELECT * FROM runs ORDER BY distance_miles DESC LIMIT ?",(limit,))
    # print_cursor_results(results)

def longest_duration_runs(limit):
    return run_query("SELECT * FROM runs ORDER BY duration_minutes DESC LIMIT ?",(limit,))
    # print_cursor_results(results)

# monthly stats
def monthly_summary(user_id,month=None):
    return run_query(load_query("monthly_summary.sql"), {"month": month,"user_id": user_id})

def yearly_summary(user_id,year=None):
    return run_query(load_query("yearly_summary.sql"),{"year": year,"user_id": user_id})

def run_type(user_id,month=None):
    return run_query(load_query("run_type.sql"), {"month": month,"user_id": user_id})
    
def max_runs(user_id,period=None):
    return run_query(load_query("max_runs.sql"), {"period": period,"user_id": user_id})

def weekly_summary(week,month):
    return run_query("""
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
    # print_cursor_results(results)
