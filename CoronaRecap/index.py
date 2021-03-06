import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import (maladies,GoogleTrend,simulateur,recap,
world,continent,country,home,pastrecessions,test)#historical,evolution,finance,


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/maladies':
        return maladies.layout
    elif pathname == '/':
        return home.layout
    # elif pathname == '/maladies/historical':
    #     return historical.layout
    # elif pathname == '/maladies/evolution':
    #     return evolution.layout
    elif pathname == '/simulation':
        return simulateur.layout
    elif pathname == '/recap':
        return recap.layout
    elif pathname == '/recap/world':
        return world.layout
    elif pathname == '/recap/continent':
        return continent.layout
    elif pathname == '/recap/country':
        return country.layout
    elif pathname == '/GoogleTrend':
        return GoogleTrend.layout
    # elif pathname == '/finance':
    #     return finance.layout
    elif pathname == '/finance/compare':
        return pastrecessions.layout
    elif pathname == '/test':
        return test.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)
