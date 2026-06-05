#!/usr/bin/env python3
from cli import parse_args
from schema import create_schema
import runs
import reports

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
            run = runs.validate_manual(args)
        runs.insert_run(run)
        print("Run inserted")
    elif args.mode == "stats":
        stat_mode = args.stat_mode
    elif args.mode == "list":
        list_mode = args.list_mode
        if list_mode == "recent":
            reports.recent_runs(args.top)
        elif list_mode == "long-dist":
            reports.longest_distance_runs(args.top)
        elif list_mode == "long-time":
            reports.longest_duration_runs(args.top)
        else:
            print("List not found")
    elif args.mode == "summary":
        if args.summary_mode == "weekly":
            print("Will implement")
        elif args.summary_mode == "monthly":
            reports.monthly_summary(args.month)
        elif args.summary_mode == "yearly":
            print("Will implement")
        elif args.summary_mode == "max":
            print("Will implement")
        elif args.summary_mode == "type":
            reports.run_type(args.month)
    else:
        print(f"Mode not found: {mode}")

if __name__ == "__main__":
    main()