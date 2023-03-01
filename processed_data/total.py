
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