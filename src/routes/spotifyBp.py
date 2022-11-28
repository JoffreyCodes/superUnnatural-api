from flask import Blueprint
from controllers.spotifyFetchController import SpotifyFetchController as sp

'''
for url_prefix '/spotify'
'''

spotifyBp = Blueprint('spotifyBp', __name__)
spotifyBp.route('/trackColor/<track_id>', methods=['GET'])(sp.get_sp_album_color)

