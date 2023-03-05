
## Libraries ##
from access_data.data_json import Data_export
import pandas as pd
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Needed for exporting information to google database.
scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
path_to_raw_data= os.environ.get("PATH_TO_RAW_DATA")
creds = ServiceAccountCredentials.from_json_keyfile_name(f"{path_to_raw_data}/creds.json",scope)
client = gspread.authorize(creds)
historical_data_database = client.open("Spotify_database").sheet1
historical_data_dates_types_types = client.open("Spotify_database").worksheet('historical_dates_types')
historical_data_dates_types_grouped = client.open("Spotify_database").worksheet('historical_dates_types_grouped')
historical_data_dates_dates = client.open("Spotify_database").worksheet('historical_dates')
historical_data_weekday_types_dataset = client.open("Spotify_database").worksheet('historical_weekday_types')
historical_data_weekday_dataset = client.open("Spotify_database").worksheet('historical_weekday')


def historical_data_with_types(save=None):
    """
    returns a dataframe with the following columns:
    ['endTime', 'artistName', 'trackName', 'msPlayed', 'typeObject', 'minutesPlayed']
    """
    historical_data = Data_export.get_historical_data() # Geting the historical information from json
    artist_podcasts = Data_export.get_episodes_data()['podcastsArtists'] # Geting the podcasts artists names from json

    typeObject = []
    for i in range(len(historical_data['artistName'])):
        if historical_data['artistName'].iloc[i] in artist_podcasts:
            typeObject.append("Podcast")
        else: typeObject.append("Track")

    historical_data['typeObject']=typeObject #Adding the type of audio
    historical_data['minutesPlayed'] = historical_data['msPlayed'] / 1000 / 60 #Turning milliseconds to minutes
    if save:
        historical_data_database.update([historical_data.columns.values.tolist()] + historical_data.values.tolist())
    historical_data['endTime'] = pd.to_datetime(historical_data['endTime'],format='%Y-%m-%d %H:%M') # Turning objects into timestamp.
    return historical_data


def historical_data_dates_types():
    """
    returns a dataframe with the following columns:
    ['date', 'typeObject', 'totalTime']
    """
    historical_data_dates_types_df = historical_data_with_types() # Getting the historical information from json
    historical_data_dates_types_df['date'] = historical_data_dates_types_df['endTime'].dt.date
    historical_data_dates_types_df['weekday'] = historical_data_dates_types_df['endTime'].dt.weekday
    historical_data_dates_types_df.drop(columns=['endTime','artistName','trackName','msPlayed'],inplace=True)
    historical_data_dates_types_df_df = historical_data_dates_types_df.groupby(['date','weekday'],as_index=False).agg(minutesPlayed=("minutesPlayed", "sum"))
    historical_data_dates_types_tracks_df = historical_data_dates_types_df.groupby(["typeObject","date","weekday"],as_index=False).agg(listeningTracks=("minutesPlayed", "sum"))
    historical_data_dates_types_types.update([historical_data_dates_types_df_df.columns.values.tolist()] + historical_data_dates_types_df_df.values.tolist())
    historical_data_dates_types_grouped.update([historical_data_dates_types_tracks_df.columns.values.tolist()]+historical_data_dates_types_tracks_df.values.tolist())

    return historical_data_dates_types_df
def historical_data_dates():
    """
    returns a dataframe with the following columns:
    ['endTime', 'artistName', 'trackName', 'msPlayed', 'typeObject', 'minutesPlayed','date]
    """
    historical_data_dates_df = historical_data_with_types() # Getting the historical information from json
    historical_data_dates_df['date'] = historical_data_dates_df['endTime'].dt.date
    music_per_day = historical_data_dates_df.groupby(['date'],as_index=False).agg(totalTime=("minutesPlayed","sum"))
    historical_data_dates_dates.update([music_per_day.columns.values.tolist()] + music_per_day.values.tolist())
    return  music_per_day

def historical_data_weekday_types():
    """
    returns a dataframe with the following columns:
    ['weekday', 'typeObject', 'totalTime']
    """
    historical_data_weekday_types_df = historical_data_with_types() # Getting the historical information from json
    historical_data_weekday_types_df['weekday'] = historical_data_weekday_types_df['endTime'].dt.weekday
    historical_data_weekday_types_df = historical_data_weekday_types_df.groupby(["weekday","typeObject"],as_index=False).agg(listeningTracks=("minutesPlayed", "sum"))
    historical_data_weekday_types_dataset.update([historical_data_weekday_types_df.columns.values.tolist()] + historical_data_weekday_types_df.values.tolist())

    return historical_data_weekday_types_df

def historical_data_weekday():
    """
    returns a dataframe with the following columns:
    ['weekday', , 'totalTime']
    """
    historical_data_weekday_df = historical_data_with_types() # Getting the historical information from json
    historical_data_weekday_df['weekday'] = historical_data_weekday_df['endTime'].dt.weekday
    historical_data_weekday_df = historical_data_weekday_df.groupby(["weekday"],as_index=False).agg(listeningTracks=("minutesPlayed", "sum"))
    historical_data_weekday_dataset.update([historical_data_weekday_df.columns.values.tolist()] + historical_data_weekday_df.values.tolist())
    return historical_data_weekday_df


historical_data_dates_types_df = historical_data_dates_types()
