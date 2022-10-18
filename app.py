import controller as ctr
from flask import Flask, jsonify
from flask_cors import CORS


'''
This app features beackend features that makes calls to 
the Supernatural api and renders a parsed out api 
for the front-end component of this app
'''


app = Flask(__name__)
CORS(app)


@app.route('/healthCheck')
def health_check():
    message = {'message': 'api is running'}
    return jsonify(message)


@app.route('/sessionId/<sessionId>')
def main_with_id(sessionId):
    api = ctr.get_sn_feed_id(sessionId)
    return jsonify(api)


@app.route('/getColor/<trackId>')
def color(trackId):
    res = ctr.get_sp_album_color(trackId)
    return jsonify(res)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
