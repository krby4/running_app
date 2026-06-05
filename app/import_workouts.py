import runs
import csv
import pathlib

def import_csv(filepath,user_id):
    path = pathlib.Path(filepath)
    with path.open(newline="",encoding="cp1252") as f:
        reader = csv.DictReader(f,delimiter=",")
        for row in reader:
            run = dict(row)
            if not run.get("duration_minutes"):
                if run.get("start_time") and run.get("end_time"):
                    run["duration_minutes"] = runs.calculate_duration_minutes(
                        run["run_date"], run["start_time"], run["end_time"]
                    )
                else:
                    run["duration_minutes"] = None
            if not run.get("start_time"):
                run["start_time"] = None
            if not run.get("end_time"):
                run["end_time"] = None
            run["distance_miles"] = float(run["distance_miles"]) if run.get("distance_miles") else None
            run["duration_minutes"] = float(run["duration_minutes"]) if run.get("duration_minutes") else None
            run["ave_hr"] = int(run["ave_hr"]) if run.get("ave_hr") else None
            run["max_hr"] = int(run["max_hr"]) if run.get("max_hr") else None
            run["rpe"] = int (run["rpe"]) if run.get("rpe") else None
            runs.insert_run(run,user_id)