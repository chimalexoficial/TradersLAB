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

columnsArray = list(df.columns.values)
print(columnsArray)


fig = go.Figure(data=[go.Table(
    header=dict(values=[columnsArray[0], columnsArray[1], columnsArray[2], columnsArray[3]],
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[df[columnsArray[0]], df[columnsArray[1]], df[columnsArray[2]], df[columnsArray[3]]],
               fill_color='lavender',
               align='left'))
])

fig.show()

#pie chart
figPie = px.pie(df, values='Count', names='Symbol')
figPie.show()

#GRAFICA DE RENDIMIENTO ANUAL VS OTROS INSTRUMENTOS
#FORMULA TCAC = ((Valor final / Valor inicial) ^ (1 / Número de años)) – 1
x = ['Trader', 'Banco', 'CETES']
y = [20, 14, 23]

# Use textposition='auto' for direct text
fig = go.Figure(data=[go.Bar(
            x=x, y=y,
            text=y,
            textposition='auto',
        )])

fig.show()



#web server
if __name__ == '__main__':
    app.run_server(debug = True)
