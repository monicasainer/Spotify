import os
import base64
from requests import post, get
import json

client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")

def get_token():
    """
    Returns the token as string.
    """
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes),"utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url,headers=headers,data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token


def get_auth_token(token):
    """
    Returns a dictionary with the authorization.
    """
    return {"Authorization": "Bearer " + token}


def search_for_episodes(token,episode_name):
    """
    returns "episode" if the input is a podcast episode. Otherwise, returns the
    name of the track.
    """
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_token(token)
    query = f"?q={episode_name}&type=episode&market=ES"

    query_url = url + query
    result = get(query_url,headers=headers)

    json_result=json.loads(result.content)
    if type(json_result)!=dict:
        return "Episode"
    else: return episode_name


def search_for_tracks(token,track_name):
    """
    Returns an array with the artist_name and the id of the track
    """
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_token(token)
    query = f"?q={track_name}&type=track&market=ES"

    query_url = url + query
    result = get(query_url,headers=headers)
    if result.status_code == 200:
        json_result=json.loads(result.content)
    # artist_name=json_result['tracks']['items'][0]['artists'][0]['name']
        track_id=json_result['tracks']['items'][0]['id']
        return track_id


def get_features_by_song(token,track_id):
    """
    Returns a dictionary with the following keys:
    'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
    'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'type',
    'id', 'uri', 'track_href', 'analysis_url', 'duration_ms', 'time_signature'
    """

    url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    headers = get_auth_token(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result
