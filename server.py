from flask import Flask
from flask import request
import time
import json

app = Flask(__name__)

@app.route('/')
def index():
    return json.dumps({ "message" : "Hello, World!" })


@app.route('/delay')
def slow():
    seconds = request.args.get('seconds', default = 5, type = int)
    time.sleep(seconds)
    return json.dumps({ "seconds" : seconds })

@app.route('/echo')
def echo():
    arg = request.args.get('message', default = "", type = str)
    return json.dumps({ "method" : request.method, "message" : arg })

@app.route('/code')
def code():
    code = request.args.get('responsecode', default = 200, type = int)
    return json.dumps({ "responsecode" : code}), code


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)