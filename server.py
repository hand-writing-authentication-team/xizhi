from flask import Flask
from flask import request
from flask import json
import sys
sys.path.append('Handwriting-Authentication-System')
import ClientModel
import os

import logging

"""
HWAT Project
"""

app = Flask(__name__)
 
@app.route("/")
def hello():
    return "Welcome to XIZHI server"

@app.route("/v1/analyze", methods=["POST"])
def analyze():
    body = request.get_json()
    if (body == None):
        data = {
            "message": "malformed json body"
        }
        response = app.response_class(
            response=json.dumps(data),
            status=400,
            mimetype='application/json'
        )
        return response
    return "", 200

@app.route("/v1/validate", methods=["POST"])
def validate():
    body = request.get_json()
    if (body == None):
        data = {
            "message": "malformed json body"
        }
        response = app.response_class(
            response=json.dumps(data),
            status=400,
            mimetype='application/json'
        )
        return response
    return "", 200
 
if __name__ == "__main__":
    Logger = logging.getLogger(__name__)
    server_host = os.environ.get("HOST")
    server_port = os.environ.get("PORT")
    Logger.setLevel(logging.DEBUG)
    if (server_host == None):
        logging.debug("server host is not set, set it as 0.0.0.0 as default")
        server_host = '0.0.0.0'
    if (server_port == None):
        logging.debug("port is not set, set it as 5000 as default")
        server_port = 5000
    server_port = int(server_port)
    app.run(host=server_host, port=server_port)