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

def test():
    # Doing our POST, will now have authorization from the server
    api_token_response = getSpotifyToken()

    parsed_api_token_json = json.loads(api_token_response.text)
    api_authorization_token = parsed_api_token_json.get('access_token')
    api_authorization_token = 'Bearer ' + api_authorization_token

    with open("all_artists.txt", "a+") as artists_file:
        for line in artists_file:
            artist = line.strip()
            print 'Currently working on %s' % (artist)
            api_request_url = 'https://api.spotify.com/v1/artists/' + artist + '/related-artists'

            # We now have our key, and new GET request for any data we want
            data_request_response = spotifyAPI(api_request_url, api_authorization_token)
            parsed_data_request_json = json.loads(data_request_response.text)

            for i in range(0, len(parsed_data_request_json['artists'])-1):
                with open("giant_artists.txt", "a+") as giant_file:
                    giant_file.write(parsed_data_request_json['artists'][i]['id'])
                    giant_file.write('\n')

            #with open("related_artists_file.txt", "w") as related_artists_file:
            #    related_artists_file.write(data_request_response.text)

            #printPaths('related_artists_file.txt')

def main(arglist):
    reload(sys)
    sys.setdefaultencoding('utf8')

    #printPaths('artists_albums_request_file.json')
    #printPaths('albums_request_file.json')
    #printPaths('audio_features_request_file.json')
    #pr1intPaths('tracks_request_file.json')
    #printPaths('artists_info_request_file.json')
    test()
    test()

if __name__ == "__main__":
    main(sys.argv[0])
