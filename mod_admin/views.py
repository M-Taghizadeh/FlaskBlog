from . import admin ### . means __init__.py
from flask import session

# important ... 
# session is a dict -----> for using session you should set a 'secret key' for your web app
# client side : Cookie,    server side : Session

@admin.route("/")
def index():
    return "Hello from admin index.."

@admin.route("/login/")
def login():
    # session["name"] = "mohammad"
    # print(session)
    # session.clear()
    # print(session.get('name'))
    return "1"