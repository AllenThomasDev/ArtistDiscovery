import dash
from dash.dependencies import Input, Output,State
from get_related import get_related
import dash_html_components as html
import pprint as pp
import dash_cytoscape as cyto
import dash_core_components as dcc
app = dash.Dash(__name__)
cyto.load_extra_layouts()
app.layout = html.Div([
        html.Div(
            className='eight columns', 
            children=[
                cyto.Cytoscape(
                    id='cytoscape',
                    layout={'name': 'breadthfirst'},
                    style={'width': '100%', 'height': '1000px'},
                    elements=[
                        {'data': {'id': '2h93pZq0e7k5yf4dywlkpM', 'label': 'Frank Ocean'}},
                    ]
                    ),
                    dcc.Dropdown(
                        id='dropdown-layout',
                        value='cose',
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
                    )]
                )
                    ])

@app.callback(Output('cytoscape', 'layout'),
              [Input('dropdown-layout', 'value')])
def update_cytoscape_layout(layout):
    return {'name': layout}

@app.callback(Output('cytoscape', 'elements'),
              [Input('cytoscape', 'tapNodeData')],
              [State('cytoscape', 'elements')])
def generate_elements(nodeData, elements):
    if nodeData:
        new_nodes,new_edges=get_related(nodeData['id'],10,0)
        for node in new_nodes:
            elements.append(node)
        for edge in new_edges:
            elements.append(edge)
        pp.pprint(new_nodes)
        # elements.append({'data': {'id': 'two', 'label': 'two'}})
        # elements.append({'data': {'source': '2h93pZq0e7k5yf4dywlkpM', 'target': 'two'}})
        print(elements)
        print(nodeData)
    return elements

if __name__ == '__main__':
    app.run_server(debug=True)