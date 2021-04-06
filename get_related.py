import spotipy
import spotipy.util as util
from credentials import credentials
user_id=credentials['user_id']
client_id=credentials['client_id']
client_secret=credentials['client_secret']
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
