from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np

within_city_aqis = []
with open("..\\data\\processed_new\\within_city_aqis.txt", 'r') as f:
    for line in f:
        line_list = line.strip().strip('][').split(', ')
        within_city_aqis.append([float(i) for i in line_list])

city_sites = []
with open("..\\data\\processed_new\\within_city_sites.txt", 'r') as f:
    for line in f:
        line_list = line.strip().strip('][').replace("'", "").split(', ')
        city_sites.append(line_list)

city_list = []
with open("..\\data\\processed_new\\city_list.txt", 'r') as f:
    for line in f:
        city_list.append(line.strip())


app = Dash(__name__)

app.layout = html.Div(children=[

    dcc.Graph(
        id='graph-with-dropdown'
    ),

    html.Label('Select City'),

    dcc.Dropdown(city_list, city_list[0], id="dropdown")
])

@app.callback(
    Output('graph-with-dropdown', 'figure'),
    Input('dropdown', 'value'))
def update_figure(selected_city):
    city_ind = np.where(np.array(city_list) == selected_city)[0][0]

    site_list = city_sites[city_ind]
    city_aqis = within_city_aqis[city_ind]

    fig = px.bar(x=site_list, y=city_aqis, labels={'x': 'Site', 'y':'Mean Normalized AQI'})

    fig.update_layout(transition_duration=500, height=800, width=1000, title_text="Within City Pollution Variation", showlegend=False)

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)