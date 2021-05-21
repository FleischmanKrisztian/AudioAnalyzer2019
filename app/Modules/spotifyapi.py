from app import application
import sys
import json
import spotipy
import time
from spotipy.oauth2 import SpotifyClientCredentials

cid = application.config["SPOTIFY_ID"]
secret = application.config["SPOTIFY_SECRET"]
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

def Get_id_of_song(search_str):
    try:
        search_str = search_str.replace('_',' ')
        search_str = ''.join([i for i in search_str if not i.isdigit()])
        result = sp.search(search_str, limit=1,type='track')
        resultstr = str(result)
        total_char = resultstr.find('}}')
        if (int(resultstr[total_char-1]) != 0 or str(resultstr[total_char-2]) != ' '):
            id_start_char = resultstr.find('spotify:track:') + 14
            id_end_char = resultstr.find('}]', id_start_char, id_start_char + 50) -1
            id_of_song = resultstr[id_start_char:id_end_char]
            return id_of_song , 200
        else:
            return ("No matches were found"), 404
    except:
        return ("Error getting match!"), 404

def key_of_id(id):
    try:
        result = str(sp.audio_features(str(id)))
        pos_of_key = result.find('key') + 6
        key_of_song = result[pos_of_key:pos_of_key+2]
        pos_of_mode = result.find('mode') + 7
        mode_of_song = int(result[pos_of_mode:pos_of_mode+1])
        if key_of_song[1] == ',':
            key_of_song = key_of_song[0]
        key_of_song_as_string = keyAsString(int(key_of_song),int(mode_of_song))
        return (key_of_song_as_string) , 200
    except:
        return('error while getting key'), 500

def keyAsString(key, mode):
    keys = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
    modes = ["Minor","Major"]
    keystring = keys[key] + " " + modes[mode]
    return keystring

def alldetails(id):
    try:
        result = sp.audio_features(str(id))
        resultstr = str(result)
        print(resultstr), 200
    except:
        return ('error while getting the details'), 500

def tempo_of_id(id):
    try:
        result = sp.audio_features(str(id))
        resultstr = str(result)
        pos_of_tempo = resultstr.find('tempo') + 8
        tempo_of_song = float(resultstr[pos_of_tempo:pos_of_tempo+3])
        tempo_of_song = round(tempo_of_song)
        return (tempo_of_song), 200
    except:
        return ('error while getting tempo'), 500