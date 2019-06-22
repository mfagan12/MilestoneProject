from flask import Flask, render_template, request
import pandas as pd
from bokeh.plotting import figure,show
from bokeh.resources import CDN
from bokeh.embed import file_html, components

app = Flask(__name__)

companies = ['AAPL', 'AMZN', 'FB', 'GOOGL', 'NFLX']

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
    
    data = pd.read_csv(url, usecols=['timestamp', 'close'])
    
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    data = data.rename({'timestamp' : 'date'}, axis = 'columns')
    
    return data

def make_plot(data, company):
    '''
    Generate components of Bokeh plot to embed in page
    Input: data - DataFrame - received from retrieve_prices call
           company - string - ticker symbol of company you want to plot
    
    '''
    p = figure(#plot_width = 500, 
               #plot_height = 300, 
               x_axis_type = 'datetime', 
               title = company + ' closing stock price')
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Price'
    p.background_fill_alpha = 0
    p.border_fill_alpha = 0
    p.ygrid.grid_line_color = 'gray'
    p.ygrid.grid_line_alpha = 0.3
    p.xgrid.grid_line_color = 'gray'
    p.xgrid.grid_line_alpha = 0.3
    p.line(data['date'], data['close'])
    script, div = components(p)
    return script, div

@app.route('/')
def index():
    # Get company and data size selections from template
    current_company = request.args.get('company')
    full = request.args.get('full')
    
    # Set default company selection
    if current_company == None:
        current_company = 'AAPL'
    
    # Make API call based on user selections and generate Bokeh components
    if full:
        data = retrieve_prices(current_company, option = 'full')
    else:
        data = retrieve_prices(current_company, option = 'compact')
    script, div = make_plot(data, current_company)
    
    # Render template with Bokeh plot
    return render_template('index.html', script = script, div = div,
                          companies = companies, current_company = current_company)

if __name__ == '__main__':
    app.run(port=5000)