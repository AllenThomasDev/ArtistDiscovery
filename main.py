from random import randint, random
import dash
from dash.dependencies import Input, Output,State
from dash_html_components.Audio import Audio
from get_related import *
import dash_html_components as html
import pprint as pp
import dash_cytoscape as cyto
import string
import random
import dash_core_components as dcc
app = dash.Dash(__name__,suppress_callback_exceptions=True)
cyto.load_extra_layouts()
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
song_dict={}
app.layout = html.Div(children=[
        html.Div(
            children=[html.Div(children=[dcc.Dropdown(id="link-input",style={'width':'100%'}, value='fra',placeholder="Who is your favorite Artist?",options=[],),
                cyto.Cytoscape(
                    id='cytoscape',
                    layout={'name': 'breadthfirst'},
                    style={'width': '100%', 'height': '1000px'},
                    elements=[]
                    )],style={'float':'left','width':'70%'}),
                    html.Div(children=[html.Div(id='artist-info-div', children=[
                        html.Img(height='320',width='320',id='Artist-Image',src='/assets\images\Question-Mark-PNG-Picture.png'),
                        html.Audio(id='preview-audio',src='',autoPlay=True,controls=True),
                        html.Div(
                            children=[
                                
                            ],id='artist-info')],style={'margin':'auto','width':'50%'}),
                    dcc.Dropdown(
                        id='dropdown-layout',
                        value='cola',
                        options=[
                            {'label':'random','value':'random'},
                            {'label':'grid','value':'grid'},
                            {'label':'circle','value':'circle'},
                            {'label':'concentric','value':'concentric'},
                            {'label':'breadthfirst','value':'breadthfirst'},
                            {'label':'cose','value':'cose'},
                            {'label':'cose-bilkent','value':'cose-bilkent'},
                            {'label':'dagre','value':'dagre'},
                            {'label':'cola','value':'cola'},
                            {'label':'klay','value':'klay'},
                            {'label':'spread','value':'spread'},
                            {'label':'euler','value':'euler'}

                        ]
                    )],style={'float':'left','width':'30%'})]
                )
                    ])

@app.callback(Output('cytoscape', 'layout'),
              [Input('dropdown-layout', 'value')])
def update_cytoscape_layout(layout):
    return {'name': layout}

@app.callback(
    Output('artist-info', 'children'),
    [Input('cytoscape','mouseoverNodeData')]
)
def update_output_div(input_value):
    l=[]
    song_options=[]
    if input_value:
        a=get_detailed_artist(input_value['id'])
        l.append(html.H3(f"{a['name']}'s top tracks are -"))
        for track in get_top_tracks(input_value['id']):
            disabled=False
            if track['audio'] == None:
                track['audio']=''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
                disabled=True
                pass
            song_options.append({'label':track['name'],'value':track['audio'],'disabled':disabled})
    song_options=sorted(song_options, key = lambda i: i['disabled'],reverse=False)
    l.append(dcc.RadioItems(id='song-list',options=song_options,labelStyle={'display': 'block'}))
    return l

@app.callback(Output('cytoscape', 'elements'),
              [Input('cytoscape', 'tapNodeData'),
              Input('link-input', 'value')],
              [State('cytoscape', 'elements')])
def generate_elements(nodeData,artistURL, elements):
    ctx = dash.callback_context
    if ctx.triggered[0]['prop_id']=='link-input.value':
        elements = [get_artist(artistURL)]
        pass
    elif ctx.triggered[0]['prop_id']=='cytoscape.tapNodeData':
        new_nodes,new_edges=get_related(nodeData['id'],10,0)
        for node in new_nodes:
            elements.append(node)
        for edge in new_edges:
            elements.append(edge)
    return elements


@app.callback(Output('Artist-Image', 'src'),
              [Input('cytoscape', 'mouseoverNodeData')])
def generate_image(mouseoverNodeData):
    if mouseoverNodeData:
        return mouseoverNodeData['url']
    return 'assets\images\Question-Mark-PNG-Picture.png'

@app.callback(Output('preview-audio', 'src'),
              [Input('song-list', 'value')])
def generate_image(song_url):
    print(song_url)
    return song_url
    
@app.callback(Output('link-input', 'options'),
              [Input('link-input', 'search_value')])
def populate_dropdown(search_query):
    options=[]
    if search_query:
        options=search_by_name(search_query)
    return options


if __name__ == '__main__':
    app.run_server(debug=True)