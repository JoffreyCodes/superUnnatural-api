from flask import Blueprint
import controllers.supernaturalFetchController as sn

'''
for url_prefix '/supernatural'
'''

supernaturalBp = Blueprint('supernaturalBp', __name__)
supernaturalBp.route('/sessionId/<sessionId>', methods=['GET'])(sn.get_sn_feed_id)

