from flask import Flask
from flask import g

from flask import request
import time
import json

app = Flask(__name__)

invocationCount = 0
healthResponseCode = 200

MESSAGE_FIELD = 'message'
DEFAULT_MESSAGE = 'Hello, World!'
SECONDS = 'seconds'
METHOD = 'method'
RESPONSECODE = 'responsecode'
COUNT = 'count'

PATH_ROOT = '/'
PATH_DELAY = '/delay'
PATH_ECHO = '/echo'
PATH_CODE = '/code'
PATH_COUNT = '/count'
PATH_HEALTH = '/health'
PATH_SET_HEALTH = '/sethealth'

@app.route(PATH_ROOT)
def index():
    return json.dumps({ MESSAGE_FIELD : DEFAULT_MESSAGE })


@app.route(PATH_DELAY)
def slow():
    seconds = request.args.get(SECONDS, default = 5, type = int)
    time.sleep(seconds)
    return json.dumps({ SECONDS : seconds })

@app.route(PATH_ECHO, methods=['GET','HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH'])
def echo():
    arg = request.args.get(MESSAGE_FIELD, default = "", type = str)
    return json.dumps({ METHOD : request.method, MESSAGE_FIELD : arg })

@app.route(PATH_CODE)
def code():
    code = request.args.get(RESPONSECODE, default = 200, type = int)
    return json.dumps({ RESPONSECODE : code}), code

@app.route(PATH_COUNT)
def count():
    global invocationCount
    invocationCount += 1
    return json.dumps({ COUNT : invocationCount}), 200

@app.route(PATH_HEALTH)
def health():
    return "", healthResponseCode

@app.route(PATH_SET_HEALTH)
def sethealth():
    code = request.args.get(RESPONSECODE, default = 200, type = int)
    global healthResponseCode
    healthResponseCode = code
    return "", 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)