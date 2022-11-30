from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go


app = Dash(__name__)

change_df = pd.read_csv("..\\data\\processed_new\\emissions_economic_change.csv")

app.layout = html.Div(children=[

    dcc.Graph(
        id='graph-with-dropdown'
    ),

    html.Label('Select City'),

    dcc.Dropdown(change_df["City"].unique(), change_df["City"].unique()[0], id="dropdown")
])

@app.callback(
    Output('graph-with-dropdown', 'figure'),
    Input('dropdown', 'value'))
def update_figure(selected_year):
    filtered_df = change_df[change_df.City == selected_year]

    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Change in Unemployment Rate", "Change in Normalized AQI"), vertical_spacing=0.05) # show change in stats or just the stats?

    fig.add_trace(
        go.Scatter(x=filtered_df["Q"], y=filtered_df["Change in Unemployment Rate"]),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(x=filtered_df["Q"], y=filtered_df["Change in Normalized AQI"]),
        row=2, col=1
    )
    # fig = px.scatter(filtered_df, x="Q", y="Economic Change")

    fig.update_layout(transition_duration=500, height=800, width=1000, title_text="Economic and Emissions Change over Quarters by City", showlegend=False)

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)