## Libraries ##

from processed_data.total import historical_data_with_types
import pandas as pd
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Needed for exporting information to google database.
scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
path_to_raw_data= os.environ.get("PATH_TO_RAW_DATA")
creds = ServiceAccountCredentials.from_json_keyfile_name(f"{path_to_raw_data}/creds.json",scope)
client = gspread.authorize(creds)
podcast_vs_tracks_classification = client.open("Spotify_database").worksheet('classification')
podcast_vs_tracks_minutes = client.open("Spotify_database").worksheet('minutes_per_month')

def aggregate_count_by_type():
    """
    returns a dataframe with the total minutes played during last year
    grouped by audio type (Podcast vs track). Columns:
    ['typeObject', 'total_minutes_played']
    """

    historical_data = historical_data_with_types()
    classification=historical_data.groupby(["typeObject"],as_index=False).agg(total_minutes_played=('minutesPlayed','sum'))
    podcast_vs_tracks_classification.update([classification.columns.values.tolist()] + classification.values.tolist())
    return classification

def minutes_per_month_and_type():
    """
    returns a dataframe with the total minutes played by month and audio type
    during last year. The columns are:
    ['monthNumber', 'month', 'typeObject', 'minutes_per_month']
    """
    historical_data = historical_data_with_types()
    historical_data['monthNumber']=historical_data["endTime"].dt.month
    historical_data['month']=historical_data["endTime"].dt.month_name()
    timeframe_listening_type = historical_data.groupby(["monthNumber","month","typeObject"],as_index=False)\
        .agg(minutes_per_month=("minutesPlayed", "sum"))
    podcast_vs_tracks_minutes.update([timeframe_listening_type.columns.values.tolist()] + timeframe_listening_type.values.tolist())

    return timeframe_listening_type
