import requests
import os

SN_FEED_API = os.getenv('SN_FEED_API')
SPOTIFY_ID_LEN = 22


class SnFetcher:

    def getTrackEmbed(track_id):
        URL = f"https://open.spotify.com/embed/track/{track_id}?utm_source=generator"
        response = requests.request(
            "GET", URL)
        return response

    def fetchSNDataWithSessionId(sessionId):
        payload = {}
        headers = {
            'Cookie': 'session_id=' + sessionId
        }
        response = requests.request(
            "GET", SN_FEED_API, headers=headers, data=payload)
        data = response.json()['data']
        return data['feed']

    def generateAPI(feed):
        apiFeed = []
        firstName = feed[0]['author']['first_name']
        lastName = feed[0]['author']['last_name']

        spotifyUrlLen = len('https://open.spotify.com/playlist/')
        for item in feed:
            itemDict = {}
            itemDict['title'] = item['workout']['title']
            itemDict['trackIdList'] = item['workout']['title']

            # Access workout object
            workout = item['workout']
            itemDict['description'] = workout['description']
            itemDict['workoutType'] = workout['workout_type']
            itemDict['isFavorite'] = workout['is_favorite']
            itemDict['launchDate'] = workout['launch_date']
            itemDict['intensity'] = workout['intensity_id']
            itemDict['duration'] = workout['duration']

            # Access body object
            body = item['body']
            itemDict['workoutId'] = body['workout_id']
            itemDict['snSongIdList'] = body['songs']

            # Access workout --> user object
            user = workout['user']
            itemDict['lastPlayed'] = user['last_played']

            # spotify parser
            spotifyUrl = workout['spotify_url']
            if(spotifyUrl is not None):
                spotifyUrl = spotifyUrl[spotifyUrlLen:spotifyUrlLen+SPOTIFY_ID_LEN]
            itemDict['spotifyPlaylistId'] = spotifyUrl

            apiFeed.append(itemDict)
        obj = {
            'data': apiFeed,
            'user':
                {
                    'firstName': firstName,
                    'lastName': lastName
                }
        }
        return obj
