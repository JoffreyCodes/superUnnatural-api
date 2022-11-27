import controller as ctr
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mysqldb import MySQL
import os


'''
This app features beackend features that makes calls to 
the Supernatural api and renders a parsed out api 
for the front-end component of this app
'''

app = Flask(__name__)
app.config.from_pyfile('config.py')
mysql = MySQL(app)
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


'''
Retrieves list of trackIds associated with a user made comment
'''


@app.route('/userNotes/<spId>', methods=['GET'])
def userNotes(spId):
    cur = mysql.connection.cursor()
    if request.method == 'GET':
        cur.execute('\
            SELECT SnTrackId \
            FROM Notes \
            WHERE SpUserId = %s\
            ', [spId])
        fetchedData = cur.fetchall()
    return jsonify(fetchedData)


'''
Retrieves comment(s) made on a specific sn track
'''


@app.route('/userNote/<spId>/<snTrackID>', methods=['GET'])
def getUserNote(spId, snTrackID):
    cur = mysql.connection.cursor()
    if request.method == 'GET':
        cur.execute('\
            SELECT * \
            FROM Notes \
            WHERE SpUserId = %s AND SnTrackID = %s \
            ORDER BY Created DESC \
            ', [spId, snTrackID])
        fetchedData = cur.fetchall()
    return jsonify(fetchedData)


'''
Delete user selected note
'''


@app.route('/delUserNote/<noteId>', methods=['DELETE'])
def delUserNote(noteId):
    cur = mysql.connection.cursor()
    if request.method == 'DELETE':
        cur.execute(' \
            DELETE FROM Notes \
            WHERE NoteId = %s \
            ', [noteId]
        )
        mysql.connection.commit()
        cur.close()
    return jsonify({'success': True}), 200, {'ContentType': 'application/json'}


'''
create and update routes for a user made note
'''


@app.route('/userNote', methods=['POST', 'PUT'])
def userNote():
    form = request.form
    noteId = form.get('NoteId')
    spUserId = form.get('SpUserId')
    snWorkoutId = form.get('SnWorkoutId')
    snTrackId = form.get('SnTrackId')
    content = form.get('Content')
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        cur.execute('\
            INSERT INTO Notes(SpUserId,SnWorkoutId, SnTrackId, Content) \
            VALUES(%s,%s,%s,%s) \
            ', [spUserId, snWorkoutId, snTrackId, content]
        )
        mysql.connection.commit()
        cur.close()
    elif request.method == 'PUT':
        cur.execute('\
            UPDATE Notes \
            SET Content = %s \
            WHERE NoteId= %s \
            ', [content, noteId]
        )
        mysql.connection.commit()
        cur.close()
    return jsonify({'success': True}), 200, {'ContentType': 'application/json'}


if __name__ == "__main__":
    app.run(debug=True)
