import os
import dash
import pandas
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime as dt

app = dash.Dash()

_DATA_PATH = "./data"
_FILE_STOCKS_NAMES = "stocks_revenue_ordered_desc.csv"

def stocks_name_list():
    result = []
    with open(_FILE_STOCKS_NAMES) as myfile:
        is_first = True
        for line in myfile:
            if is_first:
                is_first = False
                continue

            parts = line.split(";")
            if (len(parts)) >= 2:
                result.append({
                    "label": parts[0] + " - " + parts[1],
                    "value": parts[0],
                })
    #end-with
    return result

app.layout = html.Div([
    html.H1('Stock Ordered by Acumulative Revenue'),
    dcc.Dropdown(
        id='my-dropdown',
        options= stocks_name_list(),
        value='AMZN'
    ),
    dcc.Graph(id='my-graph')
])

@app.callback(Output('my-graph', 'figure'), [Input('my-dropdown', 'value')])
def update_graph(selected_dropdown_value):
    df = pandas.read_csv(os.path.join(_DATA_PATH, selected_dropdown_value))
    return {
        'data': [{
            'x': df.Date,
            'y': df.Close
        }]
    }

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)