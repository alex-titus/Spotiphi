from pprint import pprint
import requests
import ijson
import json
import time
import sys

def main(arglist):
    reload(sys)
    sys.setdefaultencoding('utf8')

    # Setting up info for our POST to the API
    api_token_headers = {
    'Authorization': 'Basic NjdjOWJkYjc4OTg1NGVmYzliMjBiNGM0YzA2Y2EwY2I6MjIxMzJmMzhiZjNlNDdiNzk0OTAzZjkzMDJiNWJlOGU=',
    }
    api_token_data = {
    'grant_type': 'client_credentials',
    }
    api_token_url = 'https://accounts.spotify.com/api/token'

    # Doing our POST, will now have authorization from the server
    api_token_response = requests.post(api_token_url, data=api_token_data, headers=api_token_headers)
    if api_token_response.status_code == 200:
        print 'Request for our API token successful.'
    else:
        print 'Request for our API token failure: ', api_token_response.status_code

    # Parse the JSON data so we can get our authorization from it
    parsed_api_token_json = json.loads(api_token_response.text)
    api_authorization_token = parsed_api_token_json.get('access_token')
    api_authorization_token = 'Bearer ' + api_authorization_token

    # Set new values for our new GET we are sending to the server
    api_request_headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': api_authorization_token
    }
    api_request_params = (
        ('country', 'ES'),
    )
    api_request_url = 'https://api.spotify.com/v1/artists/246dkjvS1zLTtiykXe5h60/albums'

    # We now have our key, and new GET request for any data we want
    data_request_response = requests.get(api_request_url, headers=api_request_headers, params=api_request_params)
    if data_request_response.status_code == 200:
        print 'Request for data from spotify successful.'
    else:
        print 'Request for data from spotify failure: ', data_request_response.status_code
    # Parse the JSON data so we can grab any information we want from it
    parsed_data_request_json = json.loads(data_request_response.text)

    with open("first_file.json", "w") as first_file:
        first_file.write(data_request_response.text)

    d = open('first_file.json', 'r')
    parser = ijson.parse(d)
    paths = sorted(set(prefix for prefix, event, value in parser if prefix))

    print 'Paths inside of parsed_data_request_json are:'
    for path in paths:
        print path

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
    #print json.dumps(parsed_data_request_json, indent=4, sort_keys=True)

    albums_request_url = 'https://api.spotify.com/v1/albums?ids=' + all_album_id_string
    # We now have our key, and new GET request for any data we want
    albums_request_response = requests.get(albums_request_url, headers=api_request_headers, params=api_request_params)

    if albums_request_response.status_code == 200:
        print 'Request for albums data from spotify successful.'
    else:
        print 'Request for albums data from spotify failure: ', albums_request_response.status_code
    parsed_album_request_json = json.loads(albums_request_response.text)

    with open("data_file.json", "w") as data_file:
        data_file.write(albums_request_response.text)

    f = open('data_file.json', 'r')
    parser = ijson.parse(f)
    paths = sorted(set(prefix for prefix, event, value in parser if prefix))

    print 'Paths inside of parsed_albums_request_json are:'
    for path in paths:
        print path

    for i in range(0, len(parsed_album_request_json['albums'])):
        print parsed_album_request_json['albums'][i]['id'].encode("utf-8")
        print parsed_album_request_json['albums'][i]['name'].encode("utf-8")
        print parsed_album_request_json['albums'][i]['release_date']
        print parsed_album_request_json['albums'][i]['popularity']
        for j in range(0, len(parsed_album_request_json['albums'][i]['tracks']['items'])):
            print parsed_album_request_json['albums'][i]['tracks']['items'][j]['id']

if __name__ == "__main__":
    main(sys.argv[0])
