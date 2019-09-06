from flask import Flask
from flask import request
from flask import json
from flask import jsonify
from utils import img_converter
import cPickle as pickle
import sys
import os

import logging
"""
To Qiushi,

About the Client Model
    *   Instance has two functionality:
        1. register: input <image list> output: <user_model, status, msg>
        2. authentication:  input <image, user_model> output: <status, msg>

I have given sample code to use the module.
And if you have any question about the code, plz feel free to knock me on WeChat.

Oh I have changed the version of some packages, plz update them using requirements.txt in both xizhi/ and Hand.../

The folder setup is like this:
- xizhi/
    - Handwriting-Authentication-System/
        - ... all auth module codes ... <you can clone github directly>
    - server.py
    - ... other stuffs in repo `xizhi`.

Fangrui 7th, Jul
"""
sys.path.append('Handwriting-Authentication-System')
from extractor import *
from detector import *
import util
from util.TranslateLayer import TranslateLayer
import ClientModel

"""
HWAT Project
"""

tmpModel = None
trsltlyr = TranslateLayer()

app = Flask(__name__)
d = ContourBox.ContourBox()

e = HarrisLBP.HarrisLBP()

authModule = ClientModel.HandWritingAuthInstance(d, e, debug=True)
 
@app.route("/")
def hello():
    return "Welcome to XIZHI server"

@app.route("/v1/analyze", methods=["POST"])
def analyze():
    """
    analyze the json and parse the info then pass them into the auth module

    NOTE:   be advised that the registration process need list of images
            which means that you need to collect all user's writing samples

    TODO:   we prefer a update to a single-shot registraction process
            we gonna work on this in the future.
    :return:
    """
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

        """
        #   Sample code
        #   `min_poi` means the tolerance in matching strategy, a hyper-parameter
        #   high `min_poi` will lead to strict matching strategy, causing possible failure in reg proc.
        #   user_model includes (reg_ratio, reg_kp, reg_feat)
        #       you can debug yourself to see the shape. They are all ND-array in numpy format
        #       The easiest way to storage user model is to dump them locally and using hash to name them.(np.load/save)
        user_model, status, status_info = authModule.register(image_list, min_poi=6)
        #   Then save the user model to the database.
        """
        return response

    handwriting_content = body["handwriting"]
    logging.info("handwriting received is {}", handwriting_content)
    cvImg = img_converter.readb64(handwriting_content)

    logging.info("getting the information {}", cvImg)
    image_list = [cvImg]
    user_model, status, status_info = authModule.register(image_list, min_poi=6)
    
    resp = {
        "user_model": trsltlyr.serialize(user_model)
    }
    return jsonify(resp), 200

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
        """
        #   Sample code
        #   auth proc only returns the status and msg
        #   but you need to load the user model in the first hand
        status, status_info = client.authenticate(test.classes[0][0], reg_info, min_poi=6)
        """
        return response

    handwriting_content = body["handwriting"]
    serialized_user_model = body["user_model"]
    user_model = trsltlyr.deserialize(serialized_user_model)
    logging.info("handwriting received is {}", handwriting_content)
    # if serialized_user_model is None:
    #     return "got not user model", 400
    # user_model = pickle.loads(serialized_user_model)
    cvImg = img_converter.readb64(handwriting_content)
    image_list = [cvImg]
    status, status_info = authModule.authenticate(cvImg, user_model, min_poi=6)
    if status:
        return "Ok", 200
    else:
        return "Not ok", 401
 
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
    app.run(host=server_host, port=server_port, debug=True)