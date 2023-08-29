import yfinance as yf


def daily_data_download(csv_list_file, start_date, end_date):
    with open(csv_list_file) as f:
        companies = f.read().splitlines()
        for company in companies:
            stock_symbol = company.split(',')[0]
            stock_name = company.split(',')[1]
            data = yf.download(stock_symbol, start=start_date, end=end_date)
            data.to_csv('datasets/daily/{}.csv'.format(stock_symbol))
