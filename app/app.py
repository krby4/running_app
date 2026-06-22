from flask import Flask,render_template,request,g,session,redirect,url_for,abort
import reports
from auth import init_auth, oauth, get_username
import auth
import runs
from datetime import datetime
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
init_auth(app)
app.wsgi_app = ProxyFix(
    app.wsgi_app,
    x_proto=1,
    x_host=1
)
# oidc = auth.create_oidc(app)

# @app.before_request
# def load_identity():
#     oidc = OpenIDConnect(app)
#     if oidc.user_loggedin:
#         g.user = g.oidc_user

#     return
@app.route("/login")
def login():
    return oauth.keycloak.authorize_redirect(
        url_for("auth_callback", _external=True)
    )
@app.route("/auth/callback")
def auth_callback():
    token = oauth.keycloak.authorize_access_token()
    session["user"] = token.get("userinfo")
    session["token"] = token
    return redirect(url_for("whoami"))
@app.route("/whoami")
def whoami():
    token = session.get("token", {})
    return {
        "user": session.get("user", {}),
        # "token_keys": list(session.get("token",{}).keys()),
        # "userinfo_keys": list(token.get("userinfo",{}).keys()),
        # "token": token,
    }

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

@app.route("/user/<user_id>/add-run", methods=["GET","POST"])
def add_run(user_id):
    if not auth.can_add_run(user_id):
        abort(403)
    if request.method == "GET":
        return render_template("add_run.html", user_id=user_id)
    
    run = runs.validate_manual(
        date=request.form.get("date"),
        start=request.form.get("start"),
        end=request.form.get("end"),
        duration=request.form.get("duration"),
        run_type=request.form.get("run_type"),
        distance=request.form.get("distance"),
        ave_hr=request.form.get("ave_hr"),
        max_hr=request.form.get("max_hr"),
        rpe=request.form.get("rpe"),
        notes=request.form.get("notes"),
    )

    runs.insert_run(run,user_id=user_id)
    return redirect(url_for("user_home",user_id=user_id))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
