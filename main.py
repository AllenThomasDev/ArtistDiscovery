import dash
from dash.dependencies import Input, Output,State
from get_related import get_artist, get_related, get_detailed_artist
import dash_html_components as html
import pprint as pp
import dash_cytoscape as cyto
import dash_core_components as dcc
app = dash.Dash(__name__)
cyto.load_extra_layouts()
app.layout = html.Div(children=[
        html.Div(
            children=[html.Div(children=[dcc.Input(id="link-input", type="text",style={'width':'100%'}, placeholder="Enter your favorite artist's Spotify URL", debounce=True),
                cyto.Cytoscape(
                    id='cytoscape',
                    layout={'name': 'breadthfirst'},
                    style={'width': '100%', 'height': '1000px'},
                    elements=[]
                    )],style={'float':'left','width':'70%'}),
                    html.Div(children=[html.Div(id='artist-info-div', children=[
                        html.Img(height='320',width='320',id='Artist-Image',src='/assets\Question-Mark-PNG-Picture.png'),
                        html.Div(id='artist-info')],style={'margin':'auto','width':'50%'}),
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
    if input_value:
        l=[]
        print(input_value)
        a=get_detailed_artist(input_value['id'])
        print(a)
        l.append(html.H3(a['name']))
        return html.H1(l)

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
    return 'assets\Question-Mark-PNG-Picture.png'

if __name__ == '__main__':
    app.run_server(debug=True)