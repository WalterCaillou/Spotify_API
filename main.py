import os
import sys
import random
import spotipy
from itertools import islice
from spotipy.oauth2 import SpotifyOAuth
import json

def create_playlist(user_id, uri):
    playlist_name = sp.playlist(uri)['name']
    create = sp.user_playlist_create(user=user_id,name=f"{playlist_name} (test)")
    # total_tracks = sp.playlist_tracks(uri)
    # print(create['id'])

    randomize_playlist(songList, create['id'])

    return "WIP"
def add_songList(playlist_uri, songList):
    items = sp.playlist_items(playlist_uri)
    tracks = items['items']
    while items['next']:
        items = sp.next(items)
        tracks.extend(items['items'])
    for song_id in tracks:
        songList.append(song_id['track']['id'])

    return "done"

def randomize_playlist(songList, playlistid):
    print(f"Randomizing Playlist!")
    random.shuffle(songList)
    # sp.playlist_add_items(playlist_id=playlist_id, items=songList)
    iterator = iter(songList)
    while chunk := list(islice(iterator, 100)):
        sp.playlist_add_items(playlistid,chunk)
    # sp.playlist_replace_items(playlist_id=playlistid, items=songList)

def delete_playlist(user_id, playlistid):
    sp.user_playlist_unfollow(user_id, playlistid[17:])
    return "Deleted previous playlist"
    
# prints out all the users playlists and returns the uri of the playlist the user chooses
def choose_playlist(playlists):
    playlist_dict = {}
    decision = True

    for i, playlist in enumerate(playlists['items']):
        print(f"{i+1}. {playlist['name']}")
        if playlist['name'] not in playlist_dict: #adds name of playlists and uri to an accessable dict
            playlist_dict[playlist['name'].lower()] = playlist['uri']

    print(f"\nWARNING!!! YOU WILL HAVE TO REDOWNLOAD THE PLAYLIST!!!\n")
    while decision:
        user_input = input("Choose a playlist to randomize: ")
        if user_input.lower() in playlist_dict:
            playlist_uri = playlist_dict[user_input]
            decision = False
        else:
            print('Playlist not found')

    return playlist_uri

if __name__ == "__main__":
    client_id = "ebc6601cc48e430b8e089ed9af792f4b"
    client_secret = "dbe9bffa0b194c9e8579ac0180a8b39a"
    # user_id = 1225275215

    scope = "playlist-modify-public user-library-read playlist-modify-private playlist-read-private"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                client_secret=client_secret,
                                                redirect_uri="http://localhost:3000",
                                                scope=scope
                                                ))
    songList = []
    user_id = sp.current_user()['id']
    playlists = sp.user_playlists(user_id)
    uri = choose_playlist(playlists)
    # print(uri)
    add_songList(uri, songList)
    create_playlist(user_id, uri)
    delete_playlist(user_id, uri)
    # randomize_playlist(songList, uri)
    # name = sp.playlist(uri)['name']
    # create_playlist(user_id, uri)

