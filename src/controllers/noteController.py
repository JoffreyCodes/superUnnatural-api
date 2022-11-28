from services.noteService import create_logic, doCreateOrUpdateNote, doDeleteNote, doGetTrackNotes, doGetUserNotedTrackIdsList


def create():
    return create_logic()


def createOrUpdateNote():
    return doCreateOrUpdateNote()


def deleteNote(noteId):
    return doDeleteNote(noteId)

def getTrackNotes(spId, snTrackId):
    return doGetTrackNotes(spId, snTrackId)

def getUserNotedTrackIdsList(spId):
    return doGetUserNotedTrackIdsList(spId)