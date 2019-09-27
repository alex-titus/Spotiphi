import requests
import json
import time
import sys
import ijson

def main(arglist):

    reload(sys)
    sys.setdefaultencoding('utf8')

    headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer BQAxMZFnRq8zN93XILaRaYfnorG4lQYHXx5TnttchH2YeqyQGa5Ju21fQk0-PXVA3Bv1hqQ2N-UzY4tH0W-koBU42OVp-yaSyArCYbxCwT6Hs3rHTr8bzyi8z-UX__DlMWdDhHUBpbSmnJl0NevpGzfW4d8tkz4DXc3GvG5GNqVuu53QCmu4hEs6SeR-SrcTRjyKZthmTqwzXvKpGoIlBmGZTcOexrg7drDRJjKv792d-1H5najFu3yxjt0p45vLxxFX2N-UljEl-CE2NPxv7OhpWjSirmYeThbIBeo',
    }

    params = (
        ('country', 'ES'),
    )

    response = requests.get('https://api.spotify.com/v1/artists/246dkjvS1zLTtiykXe5h60/albums', headers=headers, params=params)
    if response.status_code == 200:
        print 'Request successful: ', response.status_code
    else:
        print 'Request failure: ', response.status_code

    json_data = json.loads(response.text)
    dict = response.json()

    with open("data_file.json", "w") as file:
        file.write(response.text)

    
    f = open('data_file.json', 'r')
    parser = ijson.parse(f)
    paths = sorted(set(prefix for prefix, event, value in parser if prefix))

    for path in paths:
        print path


    for x in range(0, 20):
        songID = json_data['items'][x]['id']
        print(songID)

if __name__ == "__main__":
    main(sys.argv[0])
