import pandas as pd
from flask import Flask, render_template, request, redirect

from src.business_logic.process_query import create_business_logic
from src.business_logic.sp500 import accuracy_all_predictions, accuracy_val_predictions


app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello():
    return render_template("home.html")


@app.route('/get_stock_val', methods=['GET'])
def get_stock_value():
    ticker = request.args.get("ticker")
    if ticker is not None:
        bl = create_business_logic()
        prediction = bl.do_predictions_for(ticker)[-1]
        if prediction == 1:
            goal = "Buy"
        else:
            goal = "Sell"
        return render_template("stock_val.html", goal=goal, ticker=ticker)
    else:
        return render_template("stock_val.html", goal=None, ticker=None)


@app.route('/get_stock_perf', methods=['GET'])
def get_stock_perf():
    ticker = request.args.get("ticker")
    if ticker is not None:
        bl = create_business_logic()
        eval = bl.do_eval_for(ticker)
        eval_perf = round(eval*100, 2)
        return render_template("stock_perf.html", eval_perf=eval_perf, ticker=ticker)
    else:
        return render_template("stock_perf.html", eval_perf=None, ticker=None)


@app.route('/get_portfolio_perf/', methods=['GET'])
def get_portfolio_perf():
    portfolio_acc = accuracy_all_predictions()
    portfolio_acc = round(portfolio_acc* 100, 2)
    return render_template("portfolio_perf.html", portfolio_acc=portfolio_acc)


@app.route('/get_portfolio_val/', methods=['GET'])
def get_portfolio_val():
    portfolio_acc = accuracy_val_predictions()
    portfolio_acc = round(portfolio_acc* 100, 2)
    return render_template("portfolio_val.html", val_acc=portfolio_acc)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template("404.html"), 500


if __name__ == '__main__':
    # Used when running locally only. When deploying to Cloud Run,
    # a webserver process such as Gunicorn will serve the app.
    app.run(host='localhost', port=8080, debug=True)
