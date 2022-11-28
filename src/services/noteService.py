from flask import request, jsonify
from models.note import db, engine

def create_logic():
    try:
        # create tables if not exists.
        db.create_all()
        db.session.commit()
        return '==================TABLES CREATED=================='

    except Exception as e:
        print(e)
        return '==================TABLES NOT CREATED!!!=================='

def doCreateOrUpdateNote():
    form = request.form
    noteId = form.get('NoteId')
    spUserId = form.get('SpUserId')
    snWorkoutId = form.get('SnWorkoutId')
    snTrackId = form.get('SnTrackId')
    content = form.get('Content')
    if request.method == 'POST':
        stmt = f'\
            INSERT INTO Notes(SpUserId,SnWorkoutId, SnTrackId, Content) \
            VALUES( {spUserId}, {snWorkoutId}, {snTrackId}, "{content}" );'        
    elif request.method == 'PUT':
        stmt = f'\
            UPDATE Notes \
            SET Content = "{content}" \
            WHERE NoteId=  {noteId};'
    engine.execute(stmt)
    return jsonify({'success': True}), 200, {'ContentType': 'application/json'}

def doDeleteNote(noteId):
    if request.method == 'DELETE':
        stmt = f'DELETE FROM Notes WHERE NoteId = {noteId}'
        engine.execute(stmt)
        return jsonify({'success': True}), 200, {'ContentType': 'application/json'}

def doGetTrackNotes(spId, snTrackId):
    if request.method == 'GET':
        stmt = f'\
                SELECT * \
                FROM Notes \
                WHERE SpUserId = {spId} AND SnTrackID = {snTrackId} \
                ORDER BY Created DESC;'
        connection = engine.connect()
        res = connection.execute(stmt)
        return jsonify([dict(r) for r in res])

def doGetUserNotedTrackIdsList(spId):
    if request.method == 'GET':
        stmt = f'\
            SELECT DISTINCT SnTrackId \
            FROM Notes \
            WHERE SpUserId = {spId};'
    connection = engine.connect()
    res = connection.execute(stmt)
    return jsonify([dict(r) for r in res])