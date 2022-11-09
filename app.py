import controller as ctr
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mysqldb import MySQL
import os
from dotenv import load_dotenv, find_dotenv

'''
This app features beackend features that makes calls to 
the Supernatural api and renders a parsed out api 
for the front-end component of this app
'''

app = Flask(__name__)
CORS(app)
load_dotenv(find_dotenv())

app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


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


@app.route('/userNotes/<spId>', methods=['GET'])
def userNotes(spId):
    cur = mysql.connection.cursor()
    if request.method == 'GET':
        cur.execute('\
            SELECT SnTrackId \
            FROM notes \
            WHERE SpUserId = %s\
            ', [spId])
        fetchedData = cur.fetchall()
    return jsonify(fetchedData)


@app.route('/userNote/<spId>/<songId>', methods=['GET'])
def getUserNote(spId, songId):
    cur = mysql.connection.cursor()
    if request.method == 'GET':
        cur.execute('\
            SELECT * \
            FROM notes \
            WHERE SpUserId = %s AND SnTrackID = %s \
            ORDER BY Created DESC \
            ', [spId, songId])
        fetchedData = cur.fetchall()
    return jsonify(fetchedData)


@app.route('/delUserNote/<noteId>', methods=['DELETE'])
def delUserNote(noteId):
    cur = mysql.connection.cursor()
    if request.method == 'DELETE':
        print(noteId)
        cur.execute(' \
            DELETE FROM Notes \
            WHERE NoteId = %s \
            ', [noteId]
        )
        mysql.connection.commit()
        cur.close()
    return jsonify({'success': True}), 200, {'ContentType': 'application/json'}


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
    app.run(debug=True, host='0.0.0.0')
