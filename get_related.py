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
    r=(sp.artist_related_artists(artist_id)['artists'])
    sorted_r=sorted(r, key = lambda i: i['followers']['total'],reverse=True)
    a = sp.artist(artist_id)
    for x in sorted_r[0:depth]:
        nodes.append({'data': {'id': x['uri'][15:], 'label': x['name'],'url':x['images'][1]['url']}})
        edges.append({'data': {'source': artist_id, 'target': x['uri'][15:]}})
    return nodes,edges

def get_artist(artist_id):
    a = sp.artist(artist_id)
    return {'data': {'id': a['uri'][15:], 'label': a['name'],'url':a['images'][1]['url']}}

def get_detailed_artist(artist_id):
    a = sp.artist(artist_id)
    return a

def search_by_name(artist_name):
    l=[]
    d={}
    a=sp.search(artist_name,type="artist")
    for artist in a['artists']['items']:
        l.append({'label':artist['name'],'value':artist['id']})
    return l
        
def get_top_tracks(artist_id):
    l=[]
    a=sp.artist_top_tracks(artist_id)
    for track in a['tracks'][:10]:
        l.append({'name':track['name'],'audio':track['preview_url'],'cover_art':track['album']['images'][0]['url']})
    return l
    pass

