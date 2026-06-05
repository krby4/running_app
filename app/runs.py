from db import get_connection
from datetime import datetime
import csv
import io
def validate_timestamp(time):
    formats = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"]
    for fmt in formats:
        try:
            return datetime.strptime(time,fmt)
        except ValueError:
            pass
    raise ValueError(f"Could not parse time: {time}")

def calculate_duration_minutes(run_date, start_time, end_time):
    end_dt = validate_timestamp(f"{run_date} {end_time}")
    start_dt = validate_timestamp(f"{run_date} {start_time}")
    return (end_dt - start_dt).total_seconds() / 60

def validate_csv(csv_text):
    reader = csv.reader(io.StringIO(csv_text),delimiter=",")
    columns = ["run_date","start_time","end_time","run_type","distance_miles","ave_hr","max_hr","rpe","notes"]
    row = next(reader)
    if len(row) != len(columns):
        raise ValueError(f"Expected {len(columns)} fields, got {len(row)}")
    run = dict(zip(columns,row))
    run["duration_minutes"] = calculate_duration_minutes(run["run_date"],run["start_time"],run["end_time"])
    run["distance_miles"] = float(run["distance_miles"])
    run["ave_hr"] = int(run["ave_hr"])
    run["max_hr"] = int(run["max_hr"])
    run["rpe"] = int(run["rpe"])
    return run

def validate_manual(date,start=None,end=None,run_type=None,duration=None,distance=None,ave_hr=None,max_hr=None,rpe=None,notes=None):
    if duration is None and start and end:
        duration = calculate_duration_minutes(date, start, end)
    run = {"run_date" : date,
        "start_time" : start,
        "end_time" : end,
        "run_type" : run_type,
        "duration_minutes" : duration,
        "distance_miles" : distance,
        "ave_hr" : ave_hr,
        "max_hr" : max_hr,
        "rpe" : rpe,
        "notes" : notes}

    return run

def insert_run(run,user_id):

    conn = get_connection()
    conn.execute("""
INSERT INTO runs (
                run_date,
                start_time,
                end_time,
                run_type,
                duration_minutes,
                distance_miles,
                ave_hr,
                max_hr,
                rpe,
                notes,
                user_id
                )
                VALUES (?,?,?,?,?,?,?,?,?,?,?)
""",(
        run["run_date"],
        run["start_time"],
        run["end_time"],
        run["run_type"],
        run["duration_minutes"],
        run["distance_miles"],
        run["ave_hr"],
        run["max_hr"],
        run["rpe"],
        run["notes"],
        user_id
    )
)
    conn.commit()
    conn.close()
