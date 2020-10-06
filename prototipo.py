import pandas as pd
import plotly.express as px
import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go

from dash.dependencies import Input, Output


app = dash.Dash()

app.layout = html.Div([
                        html.H1('Hello Dash!!'),
                        #html.Div(id='OutputContainer')],
                        dcc.Dropdown(id='select_year',
                            options=[
                                {'label': '2019', 'value':2019},
                                {'label': '2020', 'value':2020}
                            ],
                            multi=False,
                            value=2019,
                            style={'width':'40%'}
                        ),
                        dcc.Dropdown(id='exito',
                            options=[
                                {'label': 'Todos', 'value':'All'},
                                {'label': 'Exitosas', 'value':'Good'},
                                {'label': 'Perdidas', 'value':'Bad'}
                            ],
                            multi=False,
                            value='All',
                            style={'width':'40%'}
                        ),
                        dcc.Dropdown(id='divisa',
                            options=[
                                {'label': 'EURUSD', 'value':'EURUSD'},
                                {'label': 'XAUUSD', 'value':'XAUUSD'},
                                {'label': 'GBPUSD', 'value':'GBPUSD'},
                                {'label': 'EURJPY', 'value':'EURJPY'},
                                {'label': 'USDCAD', 'value':'USDCAD'},
                                {'label': 'USDJPY', 'value':'USDJPY'},
                                {'label': 'SUDMXN', 'value':'SUDMXN'},
                                {'label': 'GBPJPY', 'value':'GBPJPY'},
                                {'label': 'AUDUSD', 'value':'AUDUSD'},
                                {'label': 'BTCUSD', 'value':'BTCUSD'},
                                {'label': 'EURGBP', 'value':'EURGBP'}
                            ],
                            multi=True,
                            value=['EURUSD', 'XAUUSD', 'GBPUSD', 'EURJPY', 'USDCAD', 'USDJPY', 'SUDMXN', 'GBPJPY', 'AUDUSD', 'BTCUSD', 'EURGBP'],
                            style={'width':'60%'}
                        ),
                        dcc.Graph(id='figPie'),
                            html.Div([
                            html.H1('Porcentaje de historico de pares'),
                            html.Div([
                                html.P('Muestra en porcentaje la cantidad de pares que han abierto operación en su '
                                       'cuenta'),
                            ])
                        ]),
                        dcc.Graph(id='fig'),
                        html.Div([
                            html.H1('Rendimiento'),
                            html.Div([
                                html.P('Este gráfico muestra el rendimiento del capital que el trader ha tenido '
                                       'durante el inicio de operacion hasta la última operación registrada'),
                            ])
                        ]),
                        dcc.Graph(id='capital'),
                            html.Div([
                            html.H1('Efectividad por par de divisa'),
                            html.Div([
                                html.P('Este gráfico muestra la efectividad por par de divisa en las que el trader ha '
                                       'estado abriendo operaciones, es decir un 100% demuestra que todas las '
                                       'operaciones que ha abierto con ese par, han resultado en positivas'),
                            ])
                        ]),
                        dcc.Graph(id='efectividad'),
                            html.Div([
                            html.H1('Indicador de meta'),
                            html.Div([
                                html.P('El siguiente medidor indica la cantidad actual de capital ganado y lo '
                                       'faltante para la meta'),
                            ])
                        ]),
                        dcc.Graph(id='goal'),
                            html.Div([
                            html.H1('Comparativa'),
                            html.Div([
                                html.P('La siguiente gráfica realiza una comparativa sobre los tres principales '
                                       'instrumentos financieros para inversiones, un mayor porcentaje demuestra un '
                                       'mayor rendimiento'),
                            ]),
                                html.H3("Hasta ahora el trader ha ofrecido un rendimiento anual total de: ")
                                #html.h2(cap)
                        ]),
                        dcc.Graph(id='rendimiento'),
                            html.Div([
                            html.H1('Aciertos'),
                            html.Div([
                                html.P('Se muestra la cantidad de operaciones que han resultado positivas contra las '
                                       'negativas. Ojo: una mayor cantidad de operaciones ganadas contra las perdidas '
                                       'no significa rentabilidad en ganancia, todo depende del manejo de riesgo, '
                                       'ya que es posible que el trader abra 20 operaciones a 0.01 lotes que '
                                       'resultaron negativas y 1 operacion a 3 lotes que resultó positiva'),
                            ])
                        ]),
                        dcc.Graph(id='aciertos'),
                            html.Div([
                            html.H1('Profit Factor'),
                            html.Div([
                                html.P('El Profit Factor se calcula dividiendo las operaciones ganadas sobre las '
                                       'operaciones perdidas. Un valor mayor a 1 es buen indicador, menor a 0 hay que '
                                       'tener cuidado'),
                            ])
                        ]),
                        dcc.Graph(id='profitFactor')
])

@app.callback(
    [
        #Output(component_id = 'OutputContainer', component_property = 'children'),
        Output(component_id = 'figPie', component_property = 'figure'),
        Output(component_id = 'fig', component_property = 'figure'),
        Output(component_id = 'capital', component_property = 'figure'),
        Output(component_id = 'efectividad', component_property = 'figure'),
        Output(component_id = 'goal', component_property = 'figure'),
        Output(component_id='rendimiento', component_property='figure'),
        Output(component_id='aciertos', component_property='figure'),
        Output(component_id='profitFactor', component_property='figure')
    ],
    [
        Input(component_id='select_year', component_property='value'),
        Input(component_id='exito', component_property='value'),
        Input(component_id='divisa', component_property='value')
    ]
)

def update_graph (select_year, exito, divisa):
    #Work data

    df_original = pd.read_csv('tradeview.csv')
    df = df_original.copy()

    df['openTime'] = pd.to_datetime(df['openTime'])
    df['closeTime'] = pd.to_datetime(df['closeTime'])
    df['Symbol'] = df['Symbol'].str.upper()
    df['Count'] = 1
    capital_inicial = 1000
    capital_meta = 2000

    df_filtered = df.copy()
    #df_filtered = df_filtered[df_filtered['closeTime'].year == select_year]

    if exito == 'Good':
        df_filtered = df_filtered[df_filtered['Profit'] >= 0]
    elif exito == 'Bad':
        df_filtered = df_filtered[df_filtered['Profit'] < 0]
    elif exito == 'All':
        df_filtered = df_filtered

    df_filtered = df_filtered[df_filtered['Symbol'].isin(divisa)]

    columns_info = ['openTime', 'Type', 'Size', 'Symbol', 'openPrice', 'closeTime', 'closePrice', 'Profit']
    df_table = df_filtered.loc[:, columns_info]
    df_table.sort_values(by=['closeTime'], inplace=True)


    fig = go.Figure(data=[go.Table(
        header=dict(values=list(df_table.columns),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[df_table[columns_info[0]], df_table[columns_info[1]], df_table[columns_info[2]], df_table[columns_info[3]], df_table[columns_info[4]], df_table[columns_info[5]], df_table[columns_info[6]], df_table[columns_info[7]]],
                fill_color='lavender',
                align='left'))
    ])

    #pie chart
    figPie = px.pie(df_filtered, values='Count', names='Symbol')

    #Curva de Capital
    df_table["Capital"] = df_table["Profit"].cumsum() + capital_inicial
    curva_capital = px.line(df_table, x="closeTime", y="Capital", title='Profits')

    #Rendimiento con trader, cetes y banco
    rendPorcentualTrader = ((df["Profit"].sum())/capital_inicial)*100
    rendPorcentualCetes = 4.18
    rendPorcentualBanco = 1.17

    compArray = ['Cetes', 'Trader', 'Banco']
    figRendimiento = go.Figure([go.Bar(x=compArray, y=[rendPorcentualCetes, rendPorcentualTrader, rendPorcentualBanco])])

    #Profit Factor
    # (Ganadoras/Perdedoras) -> Superior a 1 OK!! Inferior, mala inversion
    contPositivo = 0
    contNegativo = 0
    for x in df.index:
        val = df['Profit'][x]
        if val < 0:
            contNegativo = contNegativo + 1

        else:
            contPositivo = contPositivo+1
    #print(contNegativo)
   # print(contPositivo)
    profitFactorVal = contPositivo/contNegativo
    profitFactor = go.Figure(go.Indicator(
        mode="gauge+number",
        value=profitFactorVal,
        title={'text': "Un valor mayor a 1 muestra rentabilidad"},
        gauge={'axis': {'visible': True, 'range': [0, 2]}},
        domain={'x': [0, 1], 'y': [0, 1]}
    ))


    # Recovery Factor
    # dividir la ganancia neta entre el máximo drawdown del sistema
    #df["Profit"] = pd.to_datetime(df["Profit"])

    #dfByDate = df.sort_values(by="date")
    #print(dfByDate)

    # converting to string series



    #Porcentaje de aciertos
    # Ganadoras/Perdedoras * 100
    operacionesTotales = df.shape[0]
    aciertos = (contPositivo/operacionesTotales)*100
    perdidas = (100 - aciertos)
    #print(aciertos)
    #print(operacionesTotales)

    values = [aciertos, perdidas]
    labels = ['Ganadas', 'Perdidas']

    figAciertos = go.Figure(data=[go.Pie(labels=labels, values=values)])

    #Efectividad
    efect_x = df_filtered['Symbol'].unique()
    efect_y = []
    for x in efect_x:
        df_x = df_filtered[df_filtered['Symbol'] == x]
        positivos = len(df_x[df_x['Profit'] >= 0])
        efect_y.append(( positivos / len(df_x) ) * 100)

    figBar = go.Figure([go.Bar(name='Percentage of Effectiveness', x=efect_x, y=efect_y)])
    figBar.update_layout(title_text='Percentage of Effectiveness')

    #Meta
    capital_actual = capital_inicial + df['Profit'].sum()
    #fig = go.Figure(go.Indicator(
    #    mode = "gauge+number",
    #    value = capital_actual,
    #    reference = capital_inicial,
    #    title = {'text': "Meta"},
    #    domain = {'x': [0, 1], 'y': [0, 1]}
    #))

    goal = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = capital_actual,
        title = {'text': "Goal"},
        gauge = { 'axis': { 'visible': True, 'range': [capital_inicial, capital_meta] } },
        domain = {'x': [0, 1], 'y': [0, 1]}
    ))

    return fig, figPie, curva_capital, figBar, goal, figRendimiento, figAciertos, profitFactor





#web server
if __name__ == '__main__':
    app.run_server(debug = True)