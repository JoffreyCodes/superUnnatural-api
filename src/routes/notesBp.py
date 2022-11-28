from flask import Blueprint
from controllers.noteController import create, createOrUpdateNote, deleteNote, getTrackNotes, getUserNotedTrackIdsList

'''
for url_prefix '/notes'
'''

notesBp = Blueprint('notesBp', __name__)
notesBp.route('/create', methods=['GET'])(create)
notesBp.route('/', methods=['PUT','POST'])(createOrUpdateNote)
notesBp.route('/<noteId>', methods=['DELETE'])(deleteNote)
notesBp.route('/<spId>/<snTrackId>', methods=['GET'])(getTrackNotes)
notesBp.route('/spId/<spId>', methods=['GET'])(getUserNotedTrackIdsList)

