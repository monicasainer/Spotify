

# One of the main formulas is in total.py.
# However I do not add it here, since it does not need modification.

from processed_data.total import historical_data_with_types
from processed_data.podcast_track import aggregate_count_by_type, minutes_per_month_and_type,minutes_per_month,minutes_per_week,music_per_week
from processed_data.moment_day import timeframe_listening_merge,timeframe_listening_count_merge
from processed_data.tracks import morning_tracks_features,evening_tracks_features,night_tracks_features


historical_data_df = historical_data_with_types("yes")
classification_df = aggregate_count_by_type()
minutes_per_month_and_type_df = minutes_per_month_and_type()
minutes_per_month_df = minutes_per_month()
minutes_per_week_df = minutes_per_week()
music_per_week_df=music_per_week()
timeframe_listening_merge_df = timeframe_listening_merge()
timeframe_listening_count_merge_df = timeframe_listening_count_merge()
morning_data_df = morning_tracks_features()
evening_data_df = evening_tracks_features()
night_data_df = night_tracks_features()
