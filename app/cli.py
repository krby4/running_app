import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Running db command line tool")
    parser.add_argument("-u","--user-id",help="User id of insert",default="keith")
    subparsers = parser.add_subparsers(dest="mode",required=True)
    subparsers.add_parser("init-db",help="Initializes the database")
    add_parser = subparsers.add_parser("add-run",help="Adds a run")
    add_subparsers = add_parser.add_subparsers(dest="add_mode",required=True)
    csv_parser = add_subparsers.add_parser("csv",help="Add a run from a csv style string")
    manual_parser = add_subparsers.add_parser("manual",help="Add a run manually entering fields")
    list_parser = subparsers.add_parser("list",help="Lists runs, defaults to 10")
    import_parser = subparsers.add_parser("import-data",help="Import raw takeout data")
    stats_parser = subparsers.add_parser("stats",help="Gives more detailed stats than summary")
    summary_parser = subparsers.add_parser("summary",help="Summarize data")
    # add specific
    csv_parser.add_argument("-c","--csv-text",help="Takes raw formatted csv's and inserts")
    manual_parser.add_argument("--start",help="Start time, ISO format",default=None)
    manual_parser.add_argument("--end",help="End time, ISO format",default=None)
    manual_parser.add_argument("--duration",help="Duration of run in minutes",default=None)
    manual_parser.add_argument("--run-type",help="Type of run",choices=["Easy","Threshold","Long","Aerobic","Race"],required=True)
    manual_parser.add_argument("--distance",help="Distance in miles",type=float,default=None)
    manual_parser.add_argument("--date",help="Date of run, ISO format",required=True)
    manual_parser.add_argument("--ave-hr",help="Average Heart Rate",default=None)
    manual_parser.add_argument("--max-hr",help="Maximum Heart Rate",default=None)
    manual_parser.add_argument("--notes",help="Raw text of notes from run",default=None)
    manual_parser.add_argument("--rpe",help="Rate of percieved exertion",default=None,type=int,choices=range(0, 11))
    # import specific
    import_parser.add_argument("--path",help="Path to zip or unzipped file, or csv")
    # list specific
    list_parser.add_argument("--list-mode",help="List mode: recent, long-dist, long-time",choices=["recent", "long-dist", "long-time"])
    # summary
    summary_parser.add_argument("-s","--summary-mode",help="Summary mode: weekly, monthly, yearly, max, type",choices=["weekly","monthly","yearly","max","type"],required=True)
    summary_parser.add_argument("--month",help="Month in iso format eg 2026-06",default=None)
    summary_parser.add_argument("--year",help="Year in iso format eg 2026",default=None)
    summary_parser.add_argument("--week",help="Shows only x weeks, default = 5",type=int,default=5)
    summary_parser.add_argument("-p","--period",help="Time period to sort by",type=int,default=None)
    # shared
    for sub in [list_parser,stats_parser]:
        sub.add_argument("--top",help="Top x for stats",type=int,default=10)
    
    return parser.parse_args()
