from pprint import pprint
import requests
import ijson
import json
import time
import sys
import time

def main(arglist):
    with open("output/album_file.csv", "a") as album_file:
        album_file.write('album_id,artist_id,album_name,album_popularity,releaste_date\n')
    with open("output/artist_file.csv", "a") as artist_file:
        artist_file.write('artist_id,artist_name,artist_genre,artist_followers,artist_popularity\n')
    with open("output/track_file.csv", "a") as track_file:
        track_file.write('track_id,album_id,artist_id,explicit,track_name,track_popularity\n')
    with open("output/audio_features_file.csv", "a") as audio_features_file:
        audio_features_file.write('artist_id,album_id,track_id,track_acousticness,track_danceability,track_duration_ms,track_energy,track_instrumentalness,track_key,track_liveness,track_loudness,track_mode,track_speechiness,track_tempo,track_time_signature,track_valence\n')

if __name__ == "__main__":
    main(sys.argv[0])
