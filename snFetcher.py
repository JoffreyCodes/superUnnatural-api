import requests
import json
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
APP_CLIENT_ID = os.getenv('APP_CLIENT_ID')
APP_CLIENT_SECRET = os.getenv('APP_CLIENT_SECRET')
SN_COOKIE = os.getenv('SN_COOKIE')
SN_FEED_API = os.getenv('SN_FEED_API')
SPOTIFY_ID_LEN = 22


class SnFetcher:

    def fetchSNData():
        snFeedUrl = SN_FEED_API
        payload = {}
        headers = {
            'Cookie': SN_COOKIE
        }
        response = requests.request(
            "GET", snFeedUrl, headers=headers, data=payload)
        data = response.json()['data']
        return data['feed']

    def fetchSNDatafile():
        with open('feed.json', 'r') as feed:
            data = json.load(feed)['data']
            return data['feed']

    def generateAPI(feed):
        apiFeed = []
        spotifyUrlLen = len('https://open.spotify.com/playlist/')
        for item in feed:
            itemDict = {}
            itemDict['title'] = item['workout']['title']

            # Access workout object
            workout = item['workout']
            itemDict['description'] = workout['description']
            itemDict['workoutType'] = workout['workout_type']
            itemDict['isFavorite'] = workout['is_favorite']
            itemDict['launchDate'] = workout['launch_date']
            itemDict['intensity'] = workout['intensity_id']
            itemDict['duration'] = workout['duration']

            # Access workout --> user object
            user = workout['user']
            itemDict['lastPlayed'] = user['last_played']

            # spotify parser
            spotifyUrl = workout['spotify_url']
            if(spotifyUrl is not None):
                spotifyUrl = spotifyUrl[spotifyUrlLen:spotifyUrlLen+SPOTIFY_ID_LEN]
            itemDict['spotifyPlaylistId'] = spotifyUrl

            apiFeed.append(itemDict)
        return {'data': apiFeed}
