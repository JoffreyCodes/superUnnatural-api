import controller as ctr
import json
from flask import Flask, url_for, redirect, jsonify
from flask_cors import CORS

import os
from dotenv import load_dotenv, find_dotenv

'''
This app features beackend features that makes calls to 
the Supernatural api the renders a parsed out version of api 
for the front-end component of this app
'''
app = Flask(__name__)
CORS(app)

app.secret_key = os.urandom(12)
app.config['SESSION_COOKIE_NAME'] = 'superunnatural cookie'
load_dotenv(find_dotenv())
TOKEN_INFO = os.getenv('token_info')


@app.route('/')
def main():
    api = ctr.get_sn_feed()
    return jsonify(api)


if __name__ == "__main__":
    app.run(debug=True)
