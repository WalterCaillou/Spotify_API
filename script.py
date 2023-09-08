from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

# def search_for_artist(token, artist_name):
#     url = " https://api.spotify.com/v1/search"
#     headers = get_auth_header(token)
#     query = f"?q={artist_name}&type=artist&limit=1"

#     query_url = url + query
#     result = get(query_url, headers = headers)
#     json_result = json.loads(result.content)["artists"]["items"]
#     if len(json_result) == 0:
#         print("No artist with this name exists...")
#         return None
    
#     return json_result[0]

# def get_songs_by_artist(token, artist_id):
#     url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
#     headers = get_auth_header(token)
#     result = get(url, headers=headers)
#     json_result = json.loads(result.content)["tracks"]
#     return json_result

def get_playlists(token, user_id):
    url = f"https://api.spotify.com/v1/users/{user_id}/playlists" # url given by spotify developer website
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["items"]
    return json_result

def choose_playlist(token, playlists):
    entry = ''
    playlistdict = {}
    while (entry.lower() != 'quit'):
        for index, playlist in enumerate(playlists):
            if playlist['name'] not in playlistdict: #checks for duplicates
                playlistdict[playlist['name'].lower()] = playlist['id'].lower() #adds an entry to the dict
            print(f"{index + 1}. {playlist['name']}")

        print(playlistdict)
        entry = input(f"Choose a playlist to randomize (q or quit to stop):\n")
        print(entry.lower())
        if entry.lower() in playlistdict: #checks if the user input exists
            print(playlist[entry.lower()])
            final = playlist[entry.lower()]
            return final
        else:
            print(f'Please enter a valid playlist. :)\n')

def randomize_playlist(token, chosen):
    url = f"https://api.spotify.com/v1/playlists/{chosen}/tracks" #access the playlist based on the id (chosen) passed in
    headers = get_auth_header(token)
    result = get(url, headers = headers)
    json_result = json.loads(result.content)["items"]
    return json_result
        

    

token = get_token()
# result = search_for_artist(token, "Slander")
# artist_id = result["id"]
# songs = get_songs_by_artist(token, artist_id)
playlists = get_playlists(token, 1225275215)
# chosen = choose_playlist(token, playlists)
print(choose_playlist(token, playlists))
# print(randomize_playlist(token, chosen))


