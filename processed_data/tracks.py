from processed_data.total import historical_data_with_types
from access_data.data_api import get_token,search_for_tracks,get_features_by_song
import pandas as pd
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
path_to_raw_data= os.environ.get("PATH_TO_RAW_DATA")
creds = ServiceAccountCredentials.from_json_keyfile_name(f"{path_to_raw_data}/creds.json",scope)
client = gspread.authorize(creds)

morning_data = client.open("Spotify_database").worksheet('morning_data')
evening_data = client.open("Spotify_database").worksheet('evening_data')
night_data = client.open("Spotify_database").worksheet('night_data')

## Morning data

def morning_tracks_features():
    """
    returns a dataframe with the features for each song played last year from 00:00h to 08:00h
    columns:
    ['trackName','artistName','total_minutes_played','track_id','danceability','energy',
    'key','loudness','mode','speechiness','acousticness','instrumentalness','liveness',
    'valence','tempo','duration_ms','time_signature']
    """

    historical_data = historical_data_with_types()
    morning_time = historical_data[(historical_data['endTime'].dt.hour>=00) & (historical_data['endTime'].dt.hour<=7)]
    morning_time_tracks = morning_time[morning_time['typeObject']=='Track']
    unique_morning_time_tracks = morning_time_tracks.groupby(["trackName","artistName"],as_index=False).agg(total_minutes_played = ("minutesPlayed","sum"))
    print("Historical Data ✅")

    #To avoid future errors:
    for i in range(len(unique_morning_time_tracks)):
        if unique_morning_time_tracks['trackName'].iloc[i]=="ASOT 1000 Los Angeles ID #002 (Mixed)":
            unique_morning_time_tracks['trackName'].iloc[i].replace("ASOT 1000 Los Angeles ID #002 (Mixed)","Turn The World Into A Dancefloor" )
        if unique_morning_time_tracks['artistName'].iloc[i]=="ID":
            unique_morning_time_tracks['artistName'].iloc[i].replace("ID","Armin van Buuren")


    # Getting the track_id
    token = get_token()
    list_tracks_id = ['0eO2zq5fjPt41BreFmiIKw'] #I include the first one to avoid errors.
    for x in range(1,len(unique_morning_time_tracks['trackName'])):
            tracking_id= search_for_tracks(token,unique_morning_time_tracks['trackName'].iloc[x])
            list_tracks_id.append(tracking_id)

    unique_morning_time_tracks['track_id']=list_tracks_id
    print("Track_id ✅")

    # Getting the features for each track id
    potential_df=[]
    for t in range(len(unique_morning_time_tracks)):
        dictionary=get_features_by_song(token,unique_morning_time_tracks['track_id'].iloc[t])
        potential_df.append(dictionary)
    unique_morning_time_tracks['features']=potential_df
    unique_morning_time_tracks_features =pd.concat((unique_morning_time_tracks,unique_morning_time_tracks['features'].apply(pd.Series)),axis=1)\
        .drop(columns=['features','type','id','uri','track_href','analysis_url','error'])
    print("Features ✅")

    unique_morning_time_tracks_features = unique_morning_time_tracks_features.dropna()

    morning_data.update([unique_morning_time_tracks_features.columns.values.tolist()] + unique_morning_time_tracks_features.values.tolist())
    print("Data Saved ✅")
    return unique_morning_time_tracks_features


## Evening data
def evening_tracks_features():
    """
    returns a dataframe with the features for each song played last year from 08:00h to 16:00h
    columns:
    ['trackName','artistName','total_minutes_played','track_id','danceability','energy',
    'key','loudness','mode','speechiness','acousticness','instrumentalness','liveness',
    'valence','tempo','duration_ms','time_signature']
    """

    historical_data = historical_data_with_types()
    evening_time=historical_data[(historical_data['endTime'].dt.hour>=8) & (historical_data['endTime'].dt.hour<=15)]
    evening_time_tracks=evening_time[evening_time['typeObject']=='Track']
    unique_evening_time_tracks = evening_time_tracks.groupby(["trackName","artistName"],as_index=False).agg(total_minutes_played = ("minutesPlayed","sum"))
    print("Historical Data ✅")

    # Getting the track_id
    token = get_token()
    list_tracks_id = []
    for x in range(len(unique_evening_time_tracks['trackName'])):
            tracking_id= search_for_tracks(token,unique_evening_time_tracks['trackName'].iloc[x])
            list_tracks_id.append(tracking_id)

    unique_evening_time_tracks['track_id']=list_tracks_id
    print("Track_id ✅")

    # Getting the features for each track id
    potential_df=[]
    for t in range(len(unique_evening_time_tracks)):
        dictionary=get_features_by_song(token,unique_evening_time_tracks['track_id'].iloc[t])
        potential_df.append(dictionary)
    unique_evening_time_tracks['features']=potential_df
    print("Features ✅")

    unique_evening_time_tracks_features= pd.concat((unique_evening_time_tracks,unique_evening_time_tracks['features'].apply(pd.Series)),axis=1)\
        .drop(columns=['features','type','id','uri','track_href','analysis_url','error'])

    unique_evening_time_tracks_features = unique_evening_time_tracks_features.dropna()

    evening_data.update([unique_evening_time_tracks_features.columns.values.tolist()] + unique_evening_time_tracks_features.values.tolist())
    print("Data Saved ✅")
    return unique_evening_time_tracks_features

## Night data

def night_tracks_features():
    """
    returns a dataframe with the features for each song played last year from 16:00h to 00:00h
    columns:
    ['trackName','artistName','total_minutes_played','track_id','danceability','energy',
    'key','loudness','mode','speechiness','acousticness','instrumentalness','liveness',
    'valence','tempo','duration_ms','time_signature']
    """

    historical_data = historical_data_with_types()
    night_time=historical_data[historical_data['endTime'].dt.hour>=16]
    night_time_tracks=night_time[night_time['typeObject']=='Track']
    unique_night_time_tracks = night_time_tracks.groupby(["trackName","artistName"],as_index=False).agg(total_minutes_played = ("minutesPlayed","sum"))
    print("Historical Data ✅")

    # Getting the track_id
    token = get_token()
    list_tracks_id = []
    for x in range(len(unique_night_time_tracks['trackName'])):
            tracking_id= search_for_tracks(token,unique_night_time_tracks['trackName'].iloc[x])
            list_tracks_id.append(tracking_id)

    unique_night_time_tracks['track_id']=list_tracks_id
    print("Track_id ✅")

    # Getting the features for each track id
    potential_df=[]
    for t in range(len(unique_night_time_tracks)):
        dictionary=get_features_by_song(token,unique_night_time_tracks['track_id'].iloc[t])
        potential_df.append(dictionary)
    unique_night_time_tracks['features']=potential_df
    print("Features ✅")

    unique_night_time_tracks_features = pd.concat((unique_night_time_tracks,unique_night_time_tracks['features'].apply(pd.Series)),axis=1)\
        .drop(columns=['features','type','id','uri','track_href','analysis_url','error'])

    unique_night_time_tracks_features = unique_night_time_tracks_features.dropna()

    night_data.update([unique_night_time_tracks_features.columns.values.tolist()] + unique_night_time_tracks_features.values.tolist())
    print("Data Saved ✅")


    return unique_night_time_tracks_features
