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

def validate_manual(args):
    duration = calculate_duration_minutes(args.date, args.start, args.end)
    # (datetime.strptime(f"{args.date} {args.end}","%Y-%m-%d %H:%M") - datetime.strptime(f"{args.date} {args.start}","%Y-%m-%d %H:%M")).total_seconds() / 60
    run = {"run_date" : args.date,
        "start_time" : args.start,
        "end_time" : args.end,
        "run_type" : args.type,
        "duration_minutes" : duration,
        "distance_miles" : args.distance,
        "ave_hr" : args.ave_hr,
        "max_hr" : args.max_hr,
        "rpe" : args.rpe,
        "notes" : args.notes}

    return run

def insert_run(run):

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
                notes
                )
                VALUES (?,?,?,?,?,?,?,?,?,?)
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
        run["notes"]
    )
)
    conn.commit()
    conn.close()
