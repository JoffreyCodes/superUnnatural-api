from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from routes.notesBp import notesBp
from routes.spotifyBp import spotifyBp
from routes.supernaturalBp import supernaturalBp


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
app.register_blueprint(spotifyBp, url_prefix='/spotify')
app.register_blueprint(supernaturalBp, url_prefix='/supernatural')

migrate = Migrate(app, db)  # Initializing the migration

@app.route('/healthCheck')
def health_check():
    message = {'message': 'api is running'}
    return jsonify(message)


# @app.route('/sessionId/<sessionId>')
# def main_with_id(sessionId):
#     api = ctr.get_sn_feed_id(sessionId)
#     return jsonify(api)


if __name__ == "__main__":
    app.run(debug=True)
