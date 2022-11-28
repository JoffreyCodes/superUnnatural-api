from services.supernaturalFetchService import SupernaturalFetchService as sn


def get_sn_feed_id(sessionId):
    sn_feed = sn.fetchSNDataWithSessionId(sessionId)
    return generateAPI(sn_feed)


def generateAPI(feed):
    SPOTIFY_ID_LEN = 22

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
