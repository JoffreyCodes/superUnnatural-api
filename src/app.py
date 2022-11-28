import controllers.controller as ctr
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from routes.notesBp import notesBp
from models.note import db


'''
This app features beackend features that makes calls to 
the Supernatural api and renders a parsed out api 
for the front-end component of this app
'''

def create_app():
    app = Flask(__name__)  # flask app object
    app.config.from_pyfile('config.py')

    db.init_app(app)  # Initializing the database
    CORS(app)
    return app


app = create_app()  # Creating the app
# Registering the blueprint
app.register_blueprint(notesBp, url_prefix='/notes')
migrate = Migrate(app, db)  # Initializing the migration

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
    app.run(debug=True)
