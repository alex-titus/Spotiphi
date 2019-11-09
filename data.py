from pprint import pprint
import requests
import ijson
import json
import time
import sys
import time

def printPaths(file):
    # Will print all the paths inside of a json file you pass it, but it MUST BE A FILE
    # you can't just pass it json text
    input_file = open(file, 'r')
    parser = ijson.parse(input_file)
    paths = sorted(set(prefix for prefix, event, value in parser if prefix))

    print ('Paths inside of %s are:' % (file))
    for path in paths:
        print path

def spotifyAPI(url, api_authorization_token):
    # Will return the entire json request from whatever URl and token you pass it,
    # so you still need to know how to parse data inside of the json
    api_request_headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': api_authorization_token
    }
    api_request_params = (
        ('country', 'ES'),
    )

    request_response = requests.get(url, headers=api_request_headers, params=api_request_params)
    if request_response.status_code == 200:
        print 'Request for our API token successful.'
    else:
        print 'Request for ', url, ' data from spotify failure: ', request_response.status_code

    return request_response

def getSpotifyToken():
    # Setting up info for our POST to the API, this will return entire JSON request for the API token
    api_token_headers = {
    'Authorization': 'Basic NjdjOWJkYjc4OTg1NGVmYzliMjBiNGM0YzA2Y2EwY2I6MjIxMzJmMzhiZjNlNDdiNzk0OTAzZjkzMDJiNWJlOGU=',
    }
    api_token_data = {
    'grant_type': 'client_credentials',
    }
    api_token_url = 'https://accounts.spotify.com/api/token'

    api_token_response = requests.post(api_token_url, data=api_token_data, headers=api_token_headers)
    if api_token_response.status_code == 200:
        print 'Request for our API token successful.'
    else:
        print 'Request for our API token failure: ', api_token_response.status_code

    return api_token_response

def main(arglist):
    reload(sys)
    sys.setdefaultencoding('utf8')
    # Doing our POST, will now have authorization from the server
    api_token_response = getSpotifyToken()

    parsed_api_token_json = json.loads(api_token_response.text)
    api_authorization_token = parsed_api_token_json.get('access_token')
    api_authorization_token = 'Bearer ' + api_authorization_token

    with open("all_artists.txt", "r") as artists_file:
        for line in artists_file:
            artist = line.strip()
            print 'Currently working on %s' % (artist)
            api_request_url = 'https://api.spotify.com/v1/artists/' + artist + '/albums'
            #api_request_url = 'https://api.spotify.com/v1/artists/246dkjvS1zLTtiykXe5h60/albums'

            # We now have our key, and new GET request for any data we want
            data_request_response = spotifyAPI(api_request_url, api_authorization_token)
            parsed_data_request_json = json.loads(data_request_response.text)

            #with open("first_file.json", "w") as first_file:
            #    first_file.write(data_request_response.text)
            #printPaths('first_file.json')

            all_album_id_string = ""
            for i in range(0, len(parsed_data_request_json['items'])):
                # We now have our specific album id and title we can iterate through
                album_id = parsed_data_request_json['items'][i]['id'].encode("utf-8")
                # artist_id = parsed_data_request_json['items'][i]['artists'][0]['id'].encode("utf-8")
                # album_name = parsed_data_request_json['items'][i]['id'].encode("utf-8")
                # print ("Title: %s, ID: %s" % (album_title, album_id))
                # Append to our string to be able to request multiple albums at the same time
                all_album_id_string += album_id
                if i != len(parsed_data_request_json['items'])-1:
                    all_album_id_string += ","

            albums_request_url = 'https://api.spotify.com/v1/albums?ids=' + all_album_id_string

            # We now have our key, and new GET request for any data we want
            albums_request_response = spotifyAPI(albums_request_url, api_authorization_token)
            parsed_album_request_json = json.loads(albums_request_response.text)

            all_track_id_string = ""
            total_track_count = 0
            for i in range(0, len(parsed_album_request_json['albums'])):
                album_name = parsed_album_request_json['albums'][i]['name'].encode("utf-8")
                album_id = parsed_data_request_json['items'][i]['id'].encode("utf-8")
                artist_id = artist_id = parsed_data_request_json['items'][i]['artists'][0]['id'].encode("utf-8")
                album_releaste_date = parsed_album_request_json['albums'][i]['release_date']
                album_popularity = parsed_album_request_json['albums'][i]['popularity']
                for j in range(0, len(parsed_album_request_json['albums'][i]['tracks']['items'])):
                    albums_track_id = parsed_album_request_json['albums'][i]['tracks']['items'][j]['id']
                    all_track_id_string += albums_track_id
                    if j != len(parsed_album_request_json['albums'][i]['tracks']['items'])-1:
                        all_track_id_string += ","
                    total_track_count += 1

                audio_features_request_url = 'https://api.spotify.com/v1/audio-features/?ids=' + all_track_id_string
                tracks_request_url = 'https://api.spotify.com/v1/tracks/?ids=' + all_track_id_string
                audio_features_request_response = spotifyAPI(audio_features_request_url, api_authorization_token)
                tracks_request_response = spotifyAPI(tracks_request_url, api_authorization_token)
                parsed_tracks_request_json = json.loads(tracks_request_response.text)
                parsed_audio_features_request_json = json.loads(audio_features_request_response.text)
                with open("album_file.txt", "a") as album_file:
                    album_file.write('Album(%s, %s, %s, %s, %s)\n' % (album_id, artist_id, album_name, album_releaste_date, album_popularity))
                for k in range(0, len(parsed_audio_features_request_json['audio_features'])):
                    track_danceability = parsed_audio_features_request_json['audio_features'][k]['danceability']
                    track_energy = parsed_audio_features_request_json['audio_features'][k]['energy']
                    track_key = parsed_audio_features_request_json['audio_features'][k]['key']
                    track_loudness = parsed_audio_features_request_json['audio_features'][k]['loudness']
                    track_speechiness = parsed_audio_features_request_json['audio_features'][k]['speechiness']
                    track_acousticness = parsed_audio_features_request_json['audio_features'][k]['acousticness']
                    track_instrumentalness = parsed_audio_features_request_json['audio_features'][k]['instrumentalness']
                    track_liveness = parsed_audio_features_request_json['audio_features'][k]['liveness']
                    track_valence = parsed_audio_features_request_json['audio_features'][k]['valence']
                    track_tempo = parsed_audio_features_request_json['audio_features'][k]['tempo']
                    track_id = parsed_audio_features_request_json['audio_features'][k]['id']
                    track_name = parsed_tracks_request_json['tracks'][k]['name'].encode("utf-8")
                    with open("track_file.txt", "a") as track_file:
                        track_file.write('Track(%s, %s, %s, %s)\n' % (track_id, album_id, artist_id, track_name))
                    with open("audio_features_file.txt", "a") as audio_features_file:
                        audio_features_file.write('audio_features(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)\n' % (artist_id, album_id, track_id, track_danceability, track_energy, track_key, track_loudness, track_speechiness, track_acousticness, track_instrumentalness, track_liveness, track_valence, track_tempo))


                all_track_id_string = ''
            all_track_id_string = all_track_id_string[:-1]
            tracks_request_url = 'https://api.spotify.com/v1/audio-features/?ids=' + all_track_id_string

            tracks_request_response = spotifyAPI(tracks_request_url, api_authorization_token)

if __name__ == "__main__":
    main(sys.argv[0])
