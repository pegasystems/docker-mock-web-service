#!/usr/bin/env python3

from gevent import monkey
monkey.patch_all()

from flask import Flask
from flask import g

import gevent
from gevent.pywsgi import WSGIServer
from prometheus_flask_exporter import PrometheusMetrics

from flask import request, redirect, url_for
import time
import json
import socket
import requests
import urllib3
import pg8000



urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)
metrics = PrometheusMetrics(app)

from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

invocationCount = 0
healthResponseCode = 200

MESSAGE_FIELD = 'message'
DEFAULT_MESSAGE = 'Hello, World!'
SECONDS = 'seconds'
METHOD = 'method'
RESPONSECODE = 'responsecode'
COUNT = 'count'
HOSTNAME = 'hostname'
HOSTIP = 'hostip'
TARGET_FIELD = 'target'
DATA_FIELD = 'data'
PORT_FIELD = 'port'
SUCCESS_FIELD = 'success'
USER_FIELD = 'user'
PASSWORD_FIELD = 'password'

PATH_ROOT = '/'
PATH_DELAY = '/delay'
PATH_ECHO = '/echo'
PATH_CODE = '/code'
PATH_COUNT = '/count'
PATH_HEALTH = '/health'
PATH_SET_HEALTH = '/sethealth'
PATH_HEADERS = '/headers'
PATH_REDIRECT = '/redirect'
PATH_HOSTINFO = '/hostinfo'
PATH_REQUEST = '/request'
PATH_TCP = '/tcp'
PATH_POSTGRES = '/postgres'

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

@app.route(PATH_HEADERS)
def headers():
    response = {}
    response['headers'] = {}

    response['headers'] = dict(request.headers)
    return json.dumps(response), 200

@app.route(PATH_HOSTINFO)
def host_info():
    hostname = socket.gethostname()
    ip_addr = socket.gethostbyname(hostname)
    return json.dumps({ HOSTNAME : hostname, HOSTIP: ip_addr }), 200

@app.route(PATH_REDIRECT)
def redir():
    return redirect(url_for("index"))

@app.route(PATH_REQUEST, methods=['POST'])
def sendRequest():

    data = json.loads(request.data)
    try:
        resp = requests.get(data[TARGET_FIELD], verify=False, timeout=5)
        return json.dumps({SUCCESS_FIELD: True, RESPONSECODE: resp.status_code, DATA_FIELD: resp.text}), 200
    except requests.exceptions.ConnectionError as ncr:
        return json.dumps({SUCCESS_FIELD: False, MESSAGE_FIELD: "connection_error"}), 200
    except ConnectionRefusedError as cr:
        return json.dumps({SUCCESS_FIELD: False, MESSAGE_FIELD: "connection_refused"}), 200
    except socket.timeout:
        return json.dumps({SUCCESS_FIELD: False, MESSAGE_FIELD: "timed_out"}), 200
    except Exception as inst:
        return json.dumps({SUCCESS_FIELD: False, MESSAGE_FIELD: str(inst)}), 200

@app.route(PATH_TCP, methods=['POST'])
def tcpConnect():
    data = json.loads(request.data)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    try:
        s.connect((data[TARGET_FIELD], data[PORT_FIELD]))
        return json.dumps({SUCCESS_FIELD: True}), 200
    except ConnectionRefusedError as cr:
        return json.dumps({SUCCESS_FIELD: False, MESSAGE_FIELD: "connection_refused"}), 200
    except socket.timeout:
        return json.dumps({SUCCESS_FIELD: False, MESSAGE_FIELD: "timed_out"}), 200
    except Exception as inst:
        return json.dumps({SUCCESS_FIELD: False, MESSAGE_FIELD: str(inst)}), 200
    finally:
        s.close()

@app.route(PATH_POSTGRES, methods=['POST'])
def testpostgres():

    conn = None
    try:
        data = json.loads(request.data)
        conn = pg8000.connect(user= data[USER_FIELD], password=data[PASSWORD_FIELD], host=data[TARGET_FIELD])
        return json.dumps({SUCCESS_FIELD: True}), 200
    except Exception as inst:
        return json.dumps({SUCCESS_FIELD: False, MESSAGE_FIELD: str(inst)}), 200
    finally:
        if conn != None:
            conn.close()

if __name__ == '__main__':

    redirect_server = WSGIServer(('0.0.0.0', 8089), app)
    redirect_server.start()

    redirect_server = WSGIServer(('0.0.0.0', 8080), app)
    redirect_server.serve_forever()
