from snFetcher import SnFetcher as sn
import spotifyInteractor as spi


def get_appended_api():
    snFeed = get_sn_feed()
    appended_tracks = append_spotify_tracks(snFeed)
    return appended_tracks


def get_sn_feed():
    sn_feed = sn.fetchSNData()
    return sn.generateAPI(sn_feed)

# TODO: Implement Pagination: 20 Consecutive calls are made for length of snFeed, implement
# iterator function when user requests for more of the feed in ui,
# or implement multithreading that does not impact the order of
# dates in the returned results (sort?), memoize previous calls to sn and spotify.


def append_spotify_tracks(snFeed):
    '''
    Appends playlist 'tracks' from spotify and saved_tracks object to the snFeed
    '''
    for playlist in snFeed['data'][0:3]:
        # for playlist in snFeed['data']:
        if not playlist['spotifyPlaylistId']:
            continue
        playlist['tracks'] = spi.get_playlist_tracks(
            playlist['spotifyPlaylistId'])

        # generate track Id list to check if spotify user has id saved
        track_ids_list = []
        for track in playlist['tracks']:
            track_ids_list.append(track['track']['id'])
        # append to snFeed our check if spotify user has id saved
        playlist['saved_tracks'] = spi.check_saved_tracks(track_ids_list)
    return snFeed