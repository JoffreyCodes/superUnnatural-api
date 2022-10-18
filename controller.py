from snFetcher import SnFetcher as sn


def get_sn_feed():
    sn_feed = sn.fetchSNData()
    return sn.generateAPI(sn_feed)


def get_sn_feed_id(sessionId):
    sn_feed = sn.fetchSNDataWithSessionId(sessionId)
    return sn.generateAPI(sn_feed)


def get_sp_album_color(track_id):
    MATCH_TEXT = "style=\"--background-color:"
    LEN_HEX_COLOR = 7
    track_embed = sn.getTrackEmbed(track_id)
    text = track_embed.text
    found = text.find(MATCH_TEXT)
    left_bound_idx = found+len(MATCH_TEXT)
    right_bound_idx = left_bound_idx + LEN_HEX_COLOR
    color_hex = text[left_bound_idx:right_bound_idx]
    obj = {'data': {'color': color_hex}}
    return obj
