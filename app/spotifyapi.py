import sys
import json
import spotipy
import time
from spotipy.oauth2 import SpotifyClientCredentials
cid = '82aafe129aff41178bcd0b6dcd4aed39'
secret = '7310d1368608421e90c8ab7169d84675'
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)



def idOfSong(search_str):
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
        result = sp.audio_features(str(id))
        resultstr = str(result)
        pos_of_key = resultstr.find('key') + 6
        key_of_song = resultstr[pos_of_key:pos_of_key+2]
        if key_of_song[1] == ',':
            key_of_song = key_of_song[0]
        return (key_of_song) , 200
    except:
        return('error while getting key')

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

    
# search = 'drake upset'
# search = 'asodiyaslidualsjxbasukyrtasldj'
# id = idOfSong(search)
# print(id)
# print(key_of_id(id[0]))
# print(tempo_of_id(id[0]))