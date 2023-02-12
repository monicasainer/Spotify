import os
import pandas as pd

class get_data:
    path= os.environ.get("PATH")
    df=pd.read_json(f'{path}StreamingHistory0')
