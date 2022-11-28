import requests

class SpotifyFetchService:
    def getTrackEmbed(track_id):
        URL = f"https://open.spotify.com/embed/track/{track_id}?utm_source=generator"
        response = requests.request(
            "GET", URL)
        return response