import os
import pandas as pd
from flask import Flask, render_template, request
from patterns import patterns
from utils import daily_data
import talib
import datetime

app = Flask(__name__)


@app.route('/')
def index():
    request_pattern = request.args.get('pattern', None)

    stocks = {}
    with open('datasets/companies.csv') as f:
        companies = f.read().splitlines()
        for company in companies:
            stock_symbol = company.split(',')[0]
            stock_name = company.split(',')[1]
            stocks[stock_symbol] = {'company': stock_name}

    if request_pattern is not None:
        datafiles = os.listdir('datasets/daily')
        empty_files = []
        # results = []

        for filename in datafiles:
            filename_symbol = filename.split('.')[0]
            df = pd.read_csv('datasets/daily/{}'.format(filename))
            ta_lib_function_pattern = getattr(talib, request_pattern)

            try:
                if len(df) < 3:
                    del stocks[filename_symbol]
                else:
                    result = ta_lib_function_pattern(df['Open'], df['High'], df['Low'], df['Close'])
                    latest_result = result.tail(1).values[0]
                    # results.append({filename_symbol: {'df_len': len(df), 'res': latest_result}})

                    if latest_result > 0:
                        stocks[filename_symbol]["pattern_sentiment"] = 'bullish'
                    elif latest_result < 0:
                        stocks[filename_symbol]["pattern_sentiment"] = 'bearish'
                    else:
                        stocks[filename_symbol]["pattern_sentiment"] = None
            except:
                pass

    return render_template('index.html', patterns_var=patterns, stocks_var=stocks, current_pattern=request_pattern)


@app.route('/snapshot')
def snapshot():
    companies_list_location = 'datasets/companies.csv'
    start_date = '2022-01-01'
    end_date = datetime.datetime.now().strftime("%Y-%m-%d")

    daily_data.daily_data_download(companies_list_location, start_date, end_date)
    return {
        'code': 'success'
    }


if __name__ == '__main__':
    app.run(debug=True)
