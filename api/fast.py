from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import pandas as pd
from processed_data.podcast_track import aggregate_count_by_type,minutes_per_month_and_type
from processed_data.moment_day import timeframe_listening , timeframe_listening_count, timeframe_listening_tracks,timeframe_listening_tracks_count,timeframe_listening_podcast,timeframe_listening_podcast_count
from processed_data.tracks import morning_tracks_features,evening_tracks_features,night_tracks_features



### NOT NEEDED ANYMORE ###
# Using main_export.py I export the data to a database in google sheet.
# This will allow us to retrieve the data faster than via API



app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# uvicorn taxifare.api.fast:app --reload
# http://localhost:8000/
# http://localhost:8000/docs

# @app.get("/")
# def root():
#     return {'greeting': 'Hello'}

@app.get("/classification")
def classification():
    classification_df = aggregate_count_by_type()
    classification_df=classification_df.to_dict(orient="records")
    return classification_df


@app.get("/type_time_listening")
def type_time_listening():
    type_time_listening_df = minutes_per_month_and_type()
    type_time_listening_df = type_time_listening_df.to_dict(orient="records")
    return type_time_listening_df

@app.get("/timeframe_listening")
def total_timeframe_listening():
    timeframe_listening_df = timeframe_listening()
    timeframe_listening_df = timeframe_listening_df.to_dict(orient="records")
    return timeframe_listening_df

@app.get("/timeframe_listening_count")
def total_timeframe_listening_count():
    timeframe_listening_count_df = timeframe_listening_count()
    timeframe_listening_count_df = timeframe_listening_count_df.to_dict(orient="records")
    return timeframe_listening_count_df

@app.get("/timeframe_listening_tracks")
def tracks_timeframe_listening():
    timeframe_listening_tracks_df = timeframe_listening_tracks()
    timeframe_listening_tracks_df = timeframe_listening_tracks_df.to_dict(orient="records")
    return timeframe_listening_tracks_df

@app.get("/timeframe_listening_tracks_count")
def tracks_timeframe_listening_count():
    timeframe_listening_tracks_count_df = timeframe_listening_tracks_count()
    timeframe_listening_tracks_count_df = timeframe_listening_tracks_count_df.to_dict(orient="records")
    return timeframe_listening_tracks_count_df

@app.get("/podcast_timeframe_listening")
def podcasts_timeframe_listening():
    timeframe_listening_podcast_df = timeframe_listening_podcast()
    timeframe_listening_podcast_df = timeframe_listening_podcast_df.to_dict(orient="records")
    return timeframe_listening_podcast_df

@app.get("/podcast_timeframe_listening_count")
def podcasts_timeframe_listening_count():
    timeframe_listening_podcast_count_df = timeframe_listening_podcast_count()
    timeframe_listening_podcast_count_df = timeframe_listening_podcast_count_df.to_dict(orient="records")
    return timeframe_listening_podcast_count_df

@app.get("/morning_tracks_features")
def features_morning_tracks():
    features_morning_tracks_df = morning_tracks_features()
    features_morning_tracks_df = features_morning_tracks_df.to_dict(orient="records")
    return features_morning_tracks_df
