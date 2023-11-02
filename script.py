import http
from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
# import spotipy
# from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
user_id = 1225275215

# def Spotipy_token():
#     return SpotifyOAuth(client_id = client_id,
#                         client_secret = client_secret,
#                         redirect_uri= http://localhost,)

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

def get_playlists(token, user_id):
    url = f"https://api.spotify.com/v1/users/{user_id}/playlists" # url given by spotify developer website
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["items"]
    return json_result

def choose_playlist(playlists):
    entry = ''
    playlistdict = {}
    while (entry.lower() != 'quit'):
        for index, playlist in enumerate(playlists):
            if playlist['name'] not in playlistdict: #checks for duplicates
                playlistdict[playlist['name'].lower()] = playlist['id'] #adds an entry to the dict
            print(f"{index + 1}. {playlist['name']}")

        entry = input(f"Choose a playlist to randomize (q or quit to stop):\n")
        if entry.lower() in playlistdict: # checks if the user input exists
            final = playlistdict[entry.lower()]
            return final
        else:
            print(f'Please enter a valid playlist.\n')

def randomizer_playlist(token, playlist_id):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks" #access the playlist based on the id (chosen) passed in
    headers = get_auth_header(token)
    result = get(url, headers = headers)
    json_result = json.loads(result.content)["items"] #json_result is the songs of the playlist
    return json_result

def create_playlist(token, user_id):
    endpoint_url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    headers = get_auth_header(token)
    # playlist_name = input("Enter a playlist name: ")
    # body = {"name": f"{playlist_name}"
    #         # "public": True
    #         }
    # response = post(url, headers=headers, data=body)
    # playlist_id = response.json()
    request_body = json.dumps({
          "name": "Indie bands like Franz Ferdinand but using Python",
          "description": "My first programmatic playlist, yooo!",
          "public": True # let's keep it between us - for now
        })
    response = post(url = endpoint_url, data = request_body, headers=headers)
    return response

    

token = get_token()
# result = search_for_artist(token, "Slander")
# artist_id = result["id"]
# songs = get_songs_by_artist(token, artist_id)
# playlists = get_playlists(token, user_id)
# playlist_id = choose_playlist(playlists)
# print(playlist_id)
print(create_playlist(token, user_id))

