from authlib.integrations.flask_client import OAuth
from flask import g, session
from dotenv import load_dotenv
import os

oauth = OAuth()

def init_auth(app):
    load_dotenv()
    app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY","default")
    oauth.init_app(app)
    oauth.register(
        name="keycloak",
        client_id = os.getenv("KEYCLOAK_CLIENT_ID","default"),
        client_secret = os.getenv("KEYCLOAK_CLIENT_SECRET","default"),
        server_metadata_url = os.getenv("KEYCLOAK_METADATA_URL","default"),
        client_kwargs={
            "scope" : "openid profile email"
        },
    )
    return oauth

def get_current_user():
    return session.get("user")

def get_username():
    user = get_current_user()
    if not user:
        return None
    return user.get("preferred_username")

def get_current_roles():
    return session.get("roles")

def is_admin():
    return False
#     roles = get_current_roles()
#     if not roles:
#         return False
#     elif "running-log-admin" in roles:
#         return True
#     else:
#         return False

def can_access_user(user_id):
    username = get_username()
    if not username:
        return False
    if is_admin():
        return True
    return username == user_id

# def require_user_access(user_id):
#     if is_admin():
#         return True
#     # elif current_user == user_id:
#     #     return True
#     else:
#         return "abort 443"