import dash
from data import StockData
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html


class WebStockView:

    def __init__(self, stock_data: StockData):
        self.stock_data = stock_data
        self.app = dash.Dash()

        self._init_web_ui()

    def _init_web_ui(self):
        
        self.app.layout = html.Div([
            html.H1('Stock List'),
            dcc.Dropdown(
                id='my-dropdown',
                options=self.stock_data.stock_list(),
                value='MSFT'
            ),
            dcc.Graph(id='my-graph')
        ])

        self.app.callback(Output('my-graph', 'figure'), [Input('my-dropdown', 'value')])(self._cb_update_graph)

    def _cb_update_graph(self, selected_dropdown_value):
        return {
            'data':  self.stock_data.history(selected_dropdown_value)
        }

    def start(self):
        self.app.run_server(port=8080, host="0.0.0.0")


def start_web(stock_data: StockData):

    app = dash.Dash()
    app.layout = html.Div([
            html.H1('Stock List'),
            dcc.Dropdown(
                id='my-dropdown',
                options=stock_data.stock_list(),
                value='MSFT'
            ),
            dcc.Graph(id='my-graph')
        ])
    
    @app.callback(Output('my-graph', 'figure'), [Input('my-dropdown', 'value')])
    def _cb_update_graph(selected_dropdown_value):
        print(selected_dropdown_value)
        return {
            'data':  stock_data.history(selected_dropdown_value)
        }

    app.run_server(port=8080, host="0.0.0.0")