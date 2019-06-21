from flask import Flask, render_template, request, redirect
import pandas as pd
from bokeh.plotting import figure,show
from bokeh.resources import CDN
from bokeh.embed import file_html

app = Flask(__name__)

def retrieve_prices(ticker, option = 'compact'):
    '''Makes an API call to Alpha Vantage to get closing stock price data.
    Input:  ticker - string - stock identifier e.g. 'AAPL' for Apple stock
            option - string - default 'compact' returns 100 rows, 'full' for all
    Output: DataFrame - closing prices and dates
    '''
    
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY' \
    + '&symbol=' + ticker \
    + '&apikey=88F1NQYAGILIXIXM' \
    + '&outputsize=' + option \
    + '&datatype=csv'
    
    data = pd.read_csv(url)
    data = data.drop(columns = ['open', 'high', 'low', 'volume'])
    
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    data = data.rename({'timestamp' : 'date'}, axis = 'columns')
    
    return data

def make_plot(data):
    p = figure(plot_width = 500, 
               plot_height = 300, 
               x_axis_type = 'datetime', 
               title = 'FB' + ' closing stock price')
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Price'
    p.line(data['date'], data['close'])
    return p

@app.route('/')
def index():
#     data = retrieve_prices('FB', option = 'compact')
#     p = make_plot(data)
#     return file_html(p, CDN, 'Share price')
    return render_template('myindex.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(port=33507)
