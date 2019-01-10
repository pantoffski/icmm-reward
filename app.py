#!/usr/bin/env python
from flask import Flask, render_template, request, jsonify, g, abort, send_file
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

img_dir = os.path.abspath("./images")
img_type = "png"

config = None

def create_json_response(data=None, statusCode=0, status=""):
    status = "Success" if statusCode == 0 else status
    resp = {"statusCode": statusCode, "status": status, "data": data}
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
    base_challenge_cert_url = config["template"]["baseChallengeCertUrl"]
    base_e_reward1_url = config["template"]["baseEReward1Url"]
    base_e_reward2_url = config["template"]["baseEReward2Url"]
    return render_template("index.html", 
        baseUrl=base_url,
        baseChallengeCertUrl=base_challenge_cert_url,
        baseEReward1Url=base_e_reward1_url,
        baseEReward2Url=base_e_reward2_url)

def check_user(user, phoneNumber):
    if user == None:
        # Not found
        return False
    assert(user["phoneNumber"][0:1] == "x" and len(user["phoneNumber"]) == 5)
    if not (user["phoneNumber"][1:] == phoneNumber):
        # Not found
        return False
    return True

@app.route("/runners/<string:bibNumber>", methods=["GET"])
def get_user():
    phoneNumber = request.form.get("pin")
    if len(phoneNumber) != 4:
        return create_json_response(status=-1, statusCode="Runner not found")

    with app.app_context():
        db = get_db()
        data = db.getUser(bibNumber)
        if check_user(data, phoneNumber) == False:
            return create_json_response(status=-1, statusCode="Runner not found")
        return jsonify(data)

@app.route("/img/challengeCert/:bibNumber", methods=["GET"])
def get_cert_img():
    phoneNumber = request.form.get("pin")
    with app.app_context():
        db = get_db()
        data = db.getUser(bibNumber)
        if check_user(data, phoneNumber) == False:
            abort(404)

        file_name = img_dir + "cert-%s" % (bibNumber)
        if not os.path.isfile(file_name):
            abort(404)

        return send_file(file_name, mimetype='image/%s' % img_type)

@app.route("/img/eReward/:templateId/:bibNumber", methods=["GET"])
def get_ereward_img():
    phoneNumber = request.form.get("pin")
    with app.app_context():
        db = get_db()
        data = db.getUser(bibNumber)
        if check_user(data, phoneNumber) == False:
            abort(404)

        file_name = img_dir + "eReward-%s-%s" % (templateId,bibNumber)
        if not os.path.isfile(file_name):
            abort(404)

        return send_file(file_name, mimetype='image/%s' % img_type)

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
