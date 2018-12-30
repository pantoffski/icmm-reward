#!/usr/bin/env python
from flask import Flask, render_template, request, jsonify, g
import json
import os
import sqlite3
from datetime import datetime, timezone, timedelta
from db import UserDB

DEFAULT_CONFIG_PATH = "./config.json"
DEFAULT_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

template_dir = os.path.abspath("./views")
app = Flask(__name__,  template_folder=template_dir, static_url_path="/static")
# Auto reload if a template file is changed
app.config["TEMPLATES_AUTO_RELOAD"] = True

config = None

def create_json_response(success, data={}):
    statusCode = 0 if success == True else -1
    resp = {"statusCode": statusCode, "data": data}
    return jsonify(data)

def get_db():
    """Function for get db inside Flask app.
    Must call this funtions inside app context and do not connect database before app run.
    Example:
        with app.app_context():
            db = get_db()
    """
    if 'db' not in g:
        UserDB.connect(config["db"]["path"])
        g.db = UserDB
    return g.db

@app.teardown_appcontext
def close_connection(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route("/static/<path:path>")
def send_js(path):
    return send_from_directory("./static", path)

@app.route("/")
def index_get():
    team_list_link = config["template"]["teamListLink"]
    base_url = config["template"]["baseUrl"]
    return render_template("index.html", 
        teamListLink=team_list_link,
        baseUrl=base_url)

def check_user(user, phoneNumber, raceCategory):
    if user == None:
        # Not found
        return False
    assert(user["phoneNumber"][0:1] == "x" and len(user["phoneNumber"]) == 5)
    if not (user["raceCategory"] == raceCategory and user["phoneNumber"][1:] == phoneNumber):
        # Not found
        return False
    return True

@app.route("/runners", methods=["POST"])
def get_user():
    bibNumber = request.form.get("bibNumber")
    phoneNumber = request.form.get("phoneNumber")
    raceCategory = request.form.get("raceCategory")
    if len(phoneNumber) != 4:
        return create_json_response(success=False) 

    with app.app_context():
        db = get_db()
        data = db.getUser(bibNumber)
        if check_user(data, phoneNumber, raceCategory) == False:
            return create_json_response(success=False)
        return create_json_response(success=True, data=data)

@app.route("/submitChallenge")
def submit_challenge():
    bibNumber = request.form.get("bibNumber")
    phoneNumber = request.form.get("phoneNumber")
    raceCategory = request.form.get("raceCategory")
    with app.app_context():
        db = get_db()
        data = db.getUser(bibNumber)
        if check_user(data, phoneNumber, raceCategory) == False:
            return create_json_response(success=False)

        # Generate URL and Certificate
        data["eRewardUrl"] = eRewardUrl

        # Save URL to database
        ret = db.setERewardUrl(bibNumber, eRewardUrl)
        if ret != True:
            return create_json_response(success=False)

        return create_json_response(success=True, data=data)

def load_json_config(config_path):
    config = None
    with open(config_path) as f:
        config = json.load(f)
    return config

def main():
    global config
    config = load_json_config(DEFAULT_CONFIG_PATH)
    server_conf = config["server"]

    debug_flag = False
    if "debug" in config["server"]:
        debug_flag = config["server"]["debug"]
    
    try:
        app.run(host=server_conf["bindAddress"], port=server_conf["port"], debug=debug_flag)
    finally:
        # Caught an interrupt or some error.
        UserDB.close()

if __name__ == "__main__":
    main()
