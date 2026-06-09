from flask import Flask,render_template,request
import reports
from datetime import datetime

app = Flask(__name__)
@app.route("/")

def hello():
    return "<p>Hello Salty Keith</p>"

@app.route("/user/<user_id>", methods=["GET"])
def user_home(user_id):
    now = datetime.now()
    current_month_string = now.strftime("%Y-%m")
    current_year_string = now.strftime("%Y")
    limit = request.args.get("limit", 10, type=int)
    month = request.args.get("month", current_month_string)
    year = request.args.get("year", current_year_string)
    period = request.args.get("period")

    recent_rows = reports.recent_runs(user_id=user_id, limit=limit)
    monthly_rows = reports.monthly_summary(user_id=user_id,month=month)
    yearly_rows = reports.yearly_summary(user_id=user_id,year=year)
    run_type_rows = reports.run_type(user_id=user_id,month=month)
    max_runs_rows = reports.max_runs(user_id=user_id,period=period)
    return render_template(
        "user_dashboard.html",
        user_id=user_id,
        limit=limit,
        month=month,
        year=year,
        period=period,
        recent_rows=recent_rows,
        monthly_rows=monthly_rows,
        yearly_rows=yearly_rows,
        run_type_rows=run_type_rows,
        max_runs_rows=max_runs_rows
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
