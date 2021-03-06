import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import numpy as np
import pandas as pd
from pytrends.request import TrendReq
import plotly.graph_objects as go
from plotly.offline import plot
from app import app


#fct
mot_base = ['coronavirus','disney plus','pornhub','nintendo switch','netflix',]
def google_trend_graph(w):
    pytrend = TrendReq()
    lst = w
    pytrend.build_payload(kw_list=lst, timeframe='today 3-m')
    interest_w = pytrend.interest_over_time() 
    fig_trend_w = go.Figure()
    for i in range(len(lst)):
        fig_trend_w.add_trace(go.Scatter(x=interest_w.index, y=interest_w.iloc[:,i], mode='lines', name=lst[i]))
    fig_trend_w.update_layout(
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            tickangle = 15,
            tickfont=dict(
                family='Arial',
                size=15,
                color='rgb(37, 37, 37)',
            ),
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='lightgray',
            showline=False,
            showticklabels=True,
            tickfont=dict(
                family='Arial',
                size=15,
                color='rgb(37, 37, 37)')
        ),
        showlegend=True,
        plot_bgcolor='white'
        )
    return fig_trend_w
fig = google_trend_graph(mot_base)

#FIGURE SLIDE COMPARAIRAISON
sidebar = html.Div(id='mySidebar',className ="sidebar",children=[
            html.A(href='/',children = [html.Img(src='../assets/png/home.png',style={'width':'32px','height':'32px','margin-left':'5.6em'}),html.Div('Home',style={
                'font-size':'14px',
                'text-align':'center'
            })],style={'background-color':'#036','margin-top':' 0px'}),
            html.A(href='/recap',children=[html.Span('Summary')],style={'text-align':'left'}),
            html.A(href='/simulation',children='SIMULATION',style={'text-align':'left'}),
            html.A(href='/maladies',children='DISEASE COMPARISON',style={'text-align':'left'}),
            html.A(href='/finance',children='FINANCE',style={'text-align':'left'}),
            html.A(href='/GoogleTrend',children='INTERNET',style={'text-align':'left'}),
        ])



layout = html.Div([
    sidebar,
    html.Div(id='main',children = [
        dbc.Row(
            [
                html.Button(id='btnOpen',className='openbtn',children='☰',n_clicks=1),
                html.Div(style={'width':'50em'}),
                html.H4('GOOGLE RESEARCH INTERESTS',style={'text-transform':'uppercase','margin-top':'20px','letter-spacing': '3px'})
            ],style={'box-shadow':'0 5px 10px 0 rgba(50,50,50,.33)'}
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                html.A([html.Div('Internet Trend'),html.Div(className='encoche',style={'top':'36px','margin-top':'0px'})],href ='/GoogleTrend',className = "sousOngletActived")
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col( 
                                    dbc.Input(debounce=True,
                                    id='search',
                                    type='search',
                                    placeholder='Search...',
                                    style={
                                        'width':'100%',
                                    }
                                ),width = 9,style={'padding-right':'0px'}),
                                dbc.Col(
                                    dbc.Button(id='BtnSearch',children=html.Img(src ='https://img.icons8.com/ios/500/search--v1.png',style = {'width':'16px','height':'16px'}),color='primary',className='ml-2')
                                ,width = 3,style={'padding-left':'0px'})
                            ],style={
                                'margin-top':'4em',
                            }
                        ),
                        dbc.Row(
                           [ dbc.Label('Choose or add words (5 choices maximum)',style={'color':'white'}),
                            html.Div("",id='msgError',style={'color':'red','text-transform':'uppercase'}),
                            html.Div(style={'margin-left':'2em'},id='containerCheckList',children = 
                                dbc.Checklist(id='checklist',
                                options =
                                    [{'label':el,'value':el} for el in mot_base],
                                style={'color':'white'},
                                value = [el for el in mot_base]
                            ),
                            ),
                            html.Div(id='test'),
                            ]
                        )
                    ],className ='sideBarOnglet',width = 2),
                dbc.Col([
                    dbc.Row("dada",style={'color':'white','margin-left':'2em','margin-top':'1em'}),
                    dcc.Graph(id='trend',figure=fig,style={'height':'850px'}),
                        
                ],style={'padding':'0px'},width = 10),
                dbc.Row(id='test')
            ]
        )
        
    ],style={'padding-top':'0px'})
])

#CALLBACKS
@app.callback(
    [Output('trend','figure'),
    Output('msgError','children')],
    [Input('checklist','value'),
    Input('checklist','options')]
)
def change_search(elements,options):
    if len(elements)>5:
        elements = element[:5]
        return google_trend_graph(elements),"Too much word selected, only 5 has been displayed"
    else:
        return google_trend_graph(elements),""
# @app.callback(
#     [Output("test",'children')],
#     [Input('search','value'),
#     Input('checklist','options'),
#     Input('checklist','value')]
# )
# def add_elements(value,options,checked):
#     print(value)
#     return value
    # cases = [el['label'] for el in options]
    # cases += value
    # return dbc.Checklist(id='checklist',
    #     options =
    #         [{'label':el,'value':el} for el in cases],
    #     style={'color':'white'},
    #     value = [el for el in checked])
    # else:
    #     return dbc.Checklist(id='checklist',
    #         options =
    #             [{'label':el,'value':el} for el in checked],
    #         style={'color':'white'},
    #         value = [el for el in checked])
@app.callback(
    [Output('test','children'),
    Output('search','value')],
    [Input('BtnSearch','n_clicks'),
    Input('checklist','options'),
    Input('checklist','value')],
    [State('search','value')]
)
def update_output(clicks,options,checked,value):
    if clicks is not None and len(value) >1:
        cases = [el['label'] for el in options]
        cases = cases + [value]
        return dbc.Checklist(id='checklist2',
            options =
                [{'label':el,'value':el} for el in cases],
            style={'color':'white'},
            value = [el for el in checked]),''
    else:
        return '',''