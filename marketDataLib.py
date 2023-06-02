import numpy as np
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go
import webbrowser as wb

def getMarketData(ticker, start, end, interval):
    if ticker == "" or ticker == " ":
        return False
    try:
        data = yf.download(tickers=ticker, start=start, end=end, interval=interval)
    except Exception as ex: #wrong ticker or incorrect time frame will result in an empty figure (no data)
        print(ex)

    #declare figure
    fig = go.Figure()

    #candlestick
    fig.add_trace(go.Candlestick(x=data.index,
                                 open=data['Open'],
                                 high=data['High'],
                                 low=data['Low'],
                                 close=data['Close'],
                                 name='market data'))

    #add titles
    fig.update_layout(title=ticker+' Live share price evolution',
                      yaxis_title='Stock Price (USD per Share)')

    #X-axes
    fig.update_xaxes(rangeslider_visible=True,
                     rangeselector=dict(buttons=list([
                         dict(count=15, label='15m', step='minute', stepmode='backward'),
                         dict(count=45, label='45m', step='minute', stepmode='backward'),
                         dict(count=1, label='HTD', step='hour', stepmode='todate'),
                         dict(count=2, label='2h', step='hour', stepmode='backward'),
                         dict(step='all')
                     ])))

    #write
    html_data = fig.to_html(full_html=True)
    with(open('marketData.html', 'w', encoding='utf-8') as htmlpage):
        htmlpage.write(html_data)

    return True