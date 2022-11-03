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


@app.route('/userNotes', methods=['GET'])
def userNotes():
    form = request.form
    snUserId = form.get('SnUserId')
    cur = mysql.connection.cursor()
    if request.method == 'GET':
        cur.execute('\
            SELECT SnTrackId FROM notes \
            WHERE SnUserId = %s \
            ', (snUserId)
        )
        fetchedData = cur.fetchall()
        return jsonify(fetchedData)


@app.route('/userNote', methods=['GET', 'POST', 'PUT', 'DELETE'])
def userNote():
    form = request.form
    commentId = form.get('CommentId')
    snUserId = form.get('SnUserId')
    snWorkoutId = form.get('SnWorkoutId')
    snTrackId = form.get('SnTrackId')
    content = form.get('Content')
    cur = mysql.connection.cursor()
    if request.method == 'GET':
        cur.execute('\
            SELECT * FROM notes \
            WHERE SnTrackId = %s AND SnUserId = %s \
            ', (snTrackId, snUserId)
        )
        fetchedData = cur.fetchall()
        return jsonify(fetchedData)
    elif request.method == 'POST':
        cur.execute('\
            INSERT INTO Notes(SnUserId,SnWorkoutId, SnTrackId, Content) \
            VALUES(%s,%s,%s,%s) \
            ', (snUserId, snWorkoutId, snTrackId, content)
        )
        mysql.connection.commit()
        cur.close()
    elif request.method == 'PUT':
        cur.execute('\
            UPDATE Notes \
            SET Content = %s \
            WHERE CommentId= %s \
            ', (content, commentId)
        )
        mysql.connection.commit()
        cur.close()
    elif request.method == 'DELETE':
        cur.execute(' \
            DELETE FROM Notes \
            WHERE CommentId = %s \
            ', (commentId)
        )
        mysql.connection.commit()
        cur.close()
    return jsonify({'success': True}), 200, {'ContentType': 'application/json'}


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
