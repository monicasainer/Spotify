from processed_data.total import historical_data_with_types
import pandas as pd
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
path_to_raw_data= os.environ.get("PATH_TO_RAW_DATA")
creds = ServiceAccountCredentials.from_json_keyfile_name(f"{path_to_raw_data}/creds.json",scope)
client = gspread.authorize(creds)

moment_day_time_listening = client.open("Spotify_database").worksheet('time_listening')
moment_day_time_count = client.open("Spotify_database").worksheet('count_listening')



def timeframe_listening():
    """
    returns a dataframe with the sum of minutes played in each timeframe for each day
    timeframes:
        00:00-08:00 (it shows up as 08:00)
        08:00-16:00 (it shows up as 16:00)
        16:00-00:00 (it shows up as 00:00)
    columns:
    [ endTime, minutesPlayed ]
    """

    # Retrieving the historical data
    historical_data = historical_data_with_types()
    historical_data.set_index("endTime",inplace=True)

    # Aggregating the timestamp 3 times per day (8hours) and getting the total
    # of minutes played for each timeframe , per day.
    timeframe_listening_df = historical_data.resample("8H").agg({"minutesPlayed":"sum"})
    timeframe_listening_df = timeframe_listening_df.reset_index()
    return timeframe_listening_df


def timeframe_listening_count():
    """
    returns a dataframe with the sum of minutes played in each timeframe for the entire year
    timeframes:
        00:00-08:00 (it shows up as 08)
        08:00-16:00 (it shows up as 16)
        16:00-00:00 (it shows up as 00)
    columns:
    [ time, total_minutes_played ]

    """
    timeframe_listening_df = timeframe_listening()

    # Aggregating the timestamp 3 times per day (8 hours) and getting the total
    # of minutes played for each timeframe.
    timeframe_listening_df['time'] = timeframe_listening_df['endTime'].dt.hour
    timeframe_listening_count_df= timeframe_listening_df.groupby(["time"],as_index=False).agg(total_minutes_played=("minutesPlayed","sum"))
    return timeframe_listening_count_df


def timeframe_listening_tracks():
    """
    returns a dataframe with the sum of minutes of tracks played each timeframe for each day
    timeframes:
        00:00-08:00 (it shows up as 08:00)
        08:00-16:00 (it shows up as 16:00)
        16:00-00:00 (it shows up as 00:00)
    columns:
    [ endTime, minutesPlayed ]
    """
    historical_data = historical_data_with_types()
    historical_data.set_index("endTime",inplace=True)
    timeframe_listening_tracks_df = historical_data[historical_data['typeObject']=='Track'].resample("8H").agg({"minutesPlayed":"sum"})
    timeframe_listening_tracks_df = timeframe_listening_tracks_df.reset_index()
    return timeframe_listening_tracks_df


def timeframe_listening_tracks_count():
    """
    returns a dataframe with the sum of minutes of tracks played during each timeframe for the entire year
    timeframes:
        00:00-08:00 (it shows up as 08)
        08:00-16:00 (it shows up as 16)
        16:00-00:00 (it shows up as 00)
    columns:
    [ time, total_minutes_played ]
    """
    timeframe_listening_tracks_df = timeframe_listening_tracks()
    timeframe_listening_tracks_df['time'] = timeframe_listening_tracks_df['endTime'].dt.hour
    timeframe_listening_tracks_count_df = timeframe_listening_tracks_df.groupby(["time"],as_index=False).agg(total_minutes_played=("minutesPlayed","sum"))

    return timeframe_listening_tracks_count_df

def timeframe_listening_podcast():
    """
    returns a dataframe with the sum of minutes of podcasts played each timeframe for each day
    timeframes:
        00:00-08:00 (it shows up as 08:00)
        08:00-16:00 (it shows up as 16:00)
        16:00-00:00 (it shows up as 00:00)
    columns:
    [ endTime, minutesPlayed ]
    """

    historical_data = historical_data_with_types()
    historical_data.set_index("endTime",inplace=True)

    timeframe_listening_podcast_df = historical_data[historical_data['typeObject']=='Podcast'].resample("8H").agg({"minutesPlayed":"sum"})
    timeframe_listening_podcast_df = timeframe_listening_podcast_df.reset_index()
    return timeframe_listening_podcast_df


def timeframe_listening_podcast_count():
    """
    returns a dataframe with the sum of minutes of podcasts played during each timeframe for the entire year
    timeframes:
        00:00-08:00 (it shows up as 08)
        08:00-16:00 (it shows up as 16)
        16:00-00:00 (it shows up as 00)
    columns:
    [ time, total_minutes_played ]
    """

    timeframe_listening_podcast_df = timeframe_listening_podcast()
    timeframe_listening_podcast_df['time'] = timeframe_listening_podcast_df['endTime'].dt.hour
    timeframe_listening_podcast_count_df = timeframe_listening_podcast_df.groupby(["time"],as_index=False).agg(total_minutes_played=("minutesPlayed","sum"))
    return timeframe_listening_podcast_count_df


def timeframe_listening_merge():
    """
    returns a dataframe with the sum of minutes played in each timeframe for each day
    and for each audio type.
    Timeframes:
        00:00-08:00 (it shows up as 08:00)
        08:00-16:00 (it shows up as 16:00)
        16:00-00:00 (it shows up as 00:00)
    columns:
    [ endTime, Total, Tracks, Podcast ]
    """

    timeframe_listening_df = timeframe_listening()
    timeframe_listening_df.rename(columns={'minutesPlayed': "Total"},inplace=True)
    timeframe_listening_tracks_df = timeframe_listening_tracks()
    timeframe_listening_tracks_df.rename(columns={'minutesPlayed': "Tracks"},inplace=True)
    timeframe_listening_podcast_df = timeframe_listening_podcast()
    timeframe_listening_podcast_df.rename(columns={'minutesPlayed': "Podcast"},inplace=True)

    timeframe_listening_df_total = pd.concat([timeframe_listening_df,timeframe_listening_tracks_df,timeframe_listening_podcast_df])
    timeframe_listening_df_total['endTime'] = timeframe_listening_df_total['endTime'].astype(str)
    timeframe_listening_df_total = timeframe_listening_df_total.fillna('')
    moment_day_time_listening.update([timeframe_listening_df_total.columns.values.tolist()] + timeframe_listening_df_total.values.tolist())

    return timeframe_listening_df_total

def timeframe_listening_count_merge():
    """
    returns a dataframe with the sum of minutes played in each timeframe for the entire year
    and per type of audio.
    timeframes:
        00:00-08:00 (it shows up as 08)
        08:00-16:00 (it shows up as 16)
        16:00-00:00 (it shows up as 00)
    columns:
    [ time, Total, Tracks, Podcast ]

    """

    timeframe_listening_count_df = timeframe_listening_count()
    timeframe_listening_count_df.rename(columns={'total_minutes_played': "Total"},inplace=True)
    timeframe_listening_tracks_count_df = timeframe_listening_tracks_count()
    timeframe_listening_tracks_count_df.rename(columns={'total_minutes_played': "Tracks"},inplace=True)
    timeframe_listening_podcast_count_df = timeframe_listening_podcast_count()
    timeframe_listening_podcast_count_df.rename(columns={'total_minutes_played': "Podcast"},inplace=True)
    timeframe_listening_count_df_total = pd.concat([timeframe_listening_count_df,timeframe_listening_tracks_count_df,timeframe_listening_podcast_count_df])
    timeframe_listening_count_df_total = timeframe_listening_count_df_total.reset_index(drop=True)
    timeframe_listening_count_df_total = timeframe_listening_count_df_total.fillna('')
    moment_day_time_count.update([timeframe_listening_count_df_total.columns.values.tolist()] + timeframe_listening_count_df_total.values.tolist())

    return timeframe_listening_count_df_total
