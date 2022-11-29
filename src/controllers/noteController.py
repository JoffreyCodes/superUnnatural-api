from services.noteService import create_logic, doCreateOrUpdateNote, doDeleteNote, doGetTrackNotes, doGetUserNotedTrackIdsList
from flask import jsonify


def create():
    return create_logic()


def createOrUpdateNote():
    return doCreateOrUpdateNote()


def deleteNote(noteId):
    return doDeleteNote(noteId)


def getTrackNotes(spId, snTrackId):
    res = doGetTrackNotes(spId, snTrackId)
    return jsonify([dict(r) for r in res])
    

def getUserNotedTrackIdsList(spId):
    res = doGetUserNotedTrackIdsList(spId)
    return jsonify([dict(r) for r in res])
