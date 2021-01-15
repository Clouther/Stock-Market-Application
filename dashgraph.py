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


@app.route('/get_stock_val/<ticker>', methods=['GET', 'POST'])
def get_stock_value(ticker):
    if request.method == "GET":
        bl = create_business_logic()
        prediction = bl.do_predictions_for(ticker)[-1]

        if prediction == 1:
            goal = "Buy"
        else:
            goal = "Sell"
    elif request.method == "POST":
        text = request.form['text']
        processed_text = text.upper()
        return redirect(f"/get_stock_val/{processed_text}", code=302)

    get_last_stock_price("AAPL", last=True)







app = dash.Dash()

appl_df = get_last_stock_price("AAPL", last=True)
appl_df_close = appl_df['close']

print(appl_df_close)

import plotly.graph_objects as go


app = dash.Dash()


data = go.Scatter(x=appl_df_close.index, y=appl_df_close.values, mode='lines',name='lines')


app.layout = html.Div([dcc.Graph(id='AAPL STOCK',
                                 figure={'data': [data],
                                 'layout':go.Layout(title='Old Faithful Eruptions')})])


if __name__ == '__main__':
    app.run_server(debug=True, port=8000)