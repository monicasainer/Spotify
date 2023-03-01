import os
import json
import pandas as pd

class Data_export:
    def __init__(self):
        return None

    def get_historical_data():
        """
        Returns a dataframe with four columns:
        ['endTime', 'artistName', 'trackName', 'msPlayed']

        """
        path_to_raw_data= os.environ.get("PATH_TO_RAW_DATA")
        df=pd.read_json(f'{path_to_raw_data}/StreamingHistory0.json')
        return df

    def get_episodes_data():
        """
        returns a list with the name of the podcast artists.
        """
        path_to_raw_data= os.environ.get("PATH_TO_RAW_DATA")
        with open(f'{path_to_raw_data}/Episodes.json') as file:
            list_episodes=json.load(file)
        return list_episodes
