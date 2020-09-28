import pandas as pd
import plotly.express as px

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go

app = dash.Dash()
df = pd.read_csv('data.csv')
app.layout = html.Div([html.H1('Hello Dash!!'),
                       html.Div('ITESO 2020')])

closeDate = df.columns.str.replace('Close Date', '')

fig = go.Figure(data=[go.Table(
    header=dict(values=list(df.columns),
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[df.CloseDate, df.Symbol, df.Action, df.Population],
               fill_color='lavender',
               align='left'))
])



#web server
if __name__ == '__main__':
    app.run_server(debug = True)
