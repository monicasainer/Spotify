import os
import pandas as pd

class Data_export:
    def __init__(self):
        return None

    def get_historical_data():
        path_to_raw_data= os.environ.get("PATH_TO_RAW_DATA")
        df=pd.read_json(f'{path_to_raw_data}/StreamingHistory0.json')
        return df
