#!/usr/bin/env python3
from cli import parse_args
from schema import create_schema
import runs
import pathlib
import reports
import import_workouts

def main():
    args = parse_args()
    mode = args.mode
    if args.mode == "init-db":
        create_schema()
        print("Database created or validated")
    elif args.mode == "add-run":
        if args.add_mode == "csv":
            run = runs.validate_csv(args.csv_text)
        elif args.add_mode == "manual":
            run = runs.validate_manual(
                args.date,args.start,args.end,
                args.run_type,args.duration,args.distance,
                args.ave_hr,args.max_hr,args.rpe,args.notes)
        runs.insert_run(run,args.user_id)
        print("Run inserted")
    elif args.mode == "import-data":
        path = pathlib.Path(args.path)
        if path.suffix == ".csv":
            import_workouts.import_csv(path,args.user_id)
        else:
            print("No other imports working yet")
    elif args.mode == "list":
        list_mode = args.list_mode
        if list_mode == "recent":
            reports.print_cursor_results(reports.recent_runs(args.user_id,args.top))
        elif list_mode == "long-dist":
            reports.print_cursor_results(reports.longest_distance_runs(args.top))
        elif list_mode == "long-time":
            reports.print_cursor_results(reports.longest_duration_runs(args.top))
        else:
            print("List not found")
    elif args.mode == "summary":
        if args.summary_mode == "monthly":
             reports.print_cursor_results(reports.monthly_summary(args.month))
        elif args.summary_mode == "yearly":
            reports.print_cursor_results(reports.yearly_summary(args.year))
        elif args.summary_mode == "type":
            reports.print_cursor_results(reports.run_type(args.month))
        elif args.summary_mode == "max":
            reports.print_cursor_results(reports.max_runs(args.period))
        elif args.summary_mode == "weekly":
            print("Will implement")
    else:
        print(f"Mode not found: {mode}")

if __name__ == "__main__":
    main()