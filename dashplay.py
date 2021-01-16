import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State
from datetime import date
from datetime import timedelta
from src.business_logic.process_query import create_business_logic
from src.business_logic.sp500 import accuracy_all_predictions, accuracy_val_predictions
from src.IO.get_data_from_yahoo import get_last_stock_price
import plotly.graph_objects as go


app = dash.Dash(__name__, server=server)

text = request.form['text']

appl_df = get_last_stock_price("AAPL", last=True)
appl_df_close = appl_df['close']

data = go.Scatter(x=appl_df_close.index, y=appl_df_close.values, mode='lines', name='lines')

app.layout = html.Div([dcc.Graph(id='stock',
                                 figure={'data': [data],
                                         'layout': go.Layout(title='AAPL')})])

if __name__ == '__main__':
    app.run_server(debug=True, port=8000)