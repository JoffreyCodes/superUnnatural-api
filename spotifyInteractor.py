import time
from flask import Flask, url_for, session, redirect
import spotipy
import os
from dotenv import load_dotenv, find_dotenv
from spotipy import SpotifyOAuth
import requests


load_dotenv(find_dotenv())
APP_CLIENT_ID = os.getenv('APP_CLIENT_ID')
APP_CLIENT_SECRET = os.getenv('APP_CLIENT_SECRET')

TOKEN_INFO = os.getenv('token_info')

'''
Used for later development in integrating spotify api to backend
TODO: Handle spotify frontend authentication for backend use.
'''


def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=APP_CLIENT_ID,
        client_secret=APP_CLIENT_SECRET,
        redirect_uri=url_for('redirect_page', _external=True),
        scope='playlist-read-private playlist-modify-private user-library-read user-library-modify'
    )


def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        raise Exception("exception error")
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if (is_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    return token_info


def check_saved_tracks(track_ids_list):
    try:
        token_info = get_token()
    except:
        print("user not logged in")
        return redirect(url_for('login', external=True))
    sp = spotipy.Spotify(auth=token_info['access_token'])
    is_saved = dict(
        zip(track_ids_list, sp.current_user_saved_tracks_contains(track_ids_list)))
    return is_saved


def get_playlist_tracks(playlistId):
    '''
    given a spotify playlist id, return the response object
    '''
    try:
        token_info = get_token()
    except:
        print("user not logged in")
        return redirect(url_for('login', external=True))
    sp = spotipy.Spotify(auth=token_info['access_token'])
    return sp.playlist_tracks(playlist_id=playlistId)['items']


def parse_playlist_track_ids(tracks):
    '''
    given a playlist_items response object, 
    return a list of the track ids in the playlist
    i.e. use for current_user_saved_tracks_contains(tracks=None)
    '''
    track_list = []
    for item in tracks['items']:
        track = item['track']
        track_list.append(track['id'])
    return track_list


def get_track_embed(track_id):
    URL = f"https://open.spotify.com/embed/track/{track_id}?utm_source=generator"
    # payload = {}
    # headers = {
    #     # 'Cookie': SN_COOKIE
    # }
    response = requests.request(
        "GET", URL)
    return response
    # data = response.json()['data']
    # return data['feed']
