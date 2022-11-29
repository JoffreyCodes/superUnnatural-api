from flask import Flask, jsonify
from flask_cors import CORS
from routes.notesBp import notesBp
from routes.spotifyBp import spotifyBp
from routes.supernaturalBp import supernaturalBp
import database as db


'''
This app features beackend features that makes calls to 
the Supernatural api and renders a parsed out api 
for the front-end component of this app
'''

def create_app():
    app = Flask(__name__)  # flask app object
    app.config.from_pyfile('config.py')

    db.initialize(app)  # Initializing the database
    CORS(app)
    return app

app = create_app()  # Creating the app
# Registering the blueprint
app.register_blueprint(notesBp, url_prefix='/notes')
app.register_blueprint(spotifyBp, url_prefix='/spotify')
app.register_blueprint(supernaturalBp, url_prefix='/supernatural')

migrate = db.migrate(app)  # Initializing the migration for model db changes

@app.route('/healthCheck')
def health_check():
    message = {'message': 'api is running'}
    return jsonify(message)


if __name__ == "__main__":
    app.run(debug=True)
