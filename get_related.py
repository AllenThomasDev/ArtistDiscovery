import spotipy
import spotipy.util as util
import pprint as pp
import pandas as pd
from tabulate import tabulate 
user_id = 'YOUR_SPOTIFY_USER_ID'
client_id='API_CLIENT_ID'
client_secret='API_SECRET_KEY'
token = util.prompt_for_user_token(user_id,
                                   'user-follow-read',
                                   client_id=client_id,
                                   client_secret=client_secret,
                                   redirect_uri='http://www.google.com/')

if token:
    sp = spotipy.Spotify(auth=token)

else:
    print("Can't get token for")

def get_related(artist_id,depth,width=0):
    nodes=[]
    edges=[]
    if depth >20:
        depth=20
    r=(sp.artist_related_artists(artist_id)['artists'][0:depth])
    a = sp.artist(artist_id)
    for x in r:
        nodes.append({'data': {'id': x['uri'][15:], 'label': x['name']}})
        edges.append({'data': {'source': artist_id, 'target': x['uri'][15:]}})
    return nodes,edges
    pass
    # global df
    # global udf
    # r=(sp.artist_related_artists(artist_id)['artists'][0:depth])
    # a = sp.artist(artist_id)
    # udf.append(a['uri'])
    # if maindict.get(a['name'])!=1:
    #     for x in r:
    #         df=df.append({'source':a['name'],'target':x['name']},ignore_index=True)
    #         udf.append(x['uri'])
    #     maindict[a['name']]=1
    #     if width!=0:
    #         for x in r:
    #             addedge(x['uri'],depth,width-1)

get_related('2h93pZq0e7k5yf4dywlkpM',20,0)