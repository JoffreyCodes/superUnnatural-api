from services.spotifyFetchService import SpotifyFetchService as sp

class SpotifyFetchController:
    def get_sp_album_color(track_id):
        # search param for html text
        MATCH_TEXT = "style=\"--background-color:"
        LEN_HEX_COLOR = 7
        # html response
        track_embed = sp.getTrackEmbed(track_id)
        # convert html res to text and perform search
        text = track_embed.text
        found = text.find(MATCH_TEXT)
        # isolate background-color
        left_bound_idx = found+len(MATCH_TEXT)
        right_bound_idx = left_bound_idx + LEN_HEX_COLOR
        color_hex = text[left_bound_idx:right_bound_idx]
        # return color as obj
        obj = {'data': {'color': color_hex}}
        return obj