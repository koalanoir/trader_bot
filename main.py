import alpaca_trade_api as tradeapi
import pandas as pd
#Alpaca API: A Python library that provides a simple interface to the Alpaca trading platform.
api = tradeapi.REST('<API Key Id>', '<Secret Access Key>', base_url='https://paper-api.alpaca.markets')

def get_data(symbol, timeframe):
    barset = api.get_barset(symbol, timeframe, limit=10)
    df = pd.DataFrame({
        'Open': [bar.o for bar in barset[symbol]],
        'High': [bar.h for bar in barset[symbol]],
        'Low': [bar.l for bar in barset[symbol]],
        'Close': [bar.c for bar in barset[symbol]],
        'Volume': [bar.v for bar in barset[symbol]]
    })
    return df

def moving_average(data, window):
    return data['Close'].rolling(window).mean()

def run_algorithm(symbol, timeframe, window):
    while True:
        data = get_data(symbol, timeframe)
        ma = moving_average(data, window)
        current_price = data['Close'].iloc[-1]
        if current_price > ma.iloc[-1]:
            api.submit_order(
                symbol=symbol,
                qty=1,
                side='buy',
                type='market',
                time_in_force='gtc'
            )
        else:
            api.submit_order(
                symbol=symbol,
                qty=1,
                side='sell',
                type='market',
                time_in_force='gtc'
            )
#This algorithm retrieves the last 10 minutes of price data for the AAPL stock, 
# calculates its 10-period moving average, and then submits a buy or sell order based on whether 
# the current price is above or below the moving average. This algorithm is for demonstration purposes only,
#  and it’s important to conduct thorough backtesting and risk management before using it with real money.
run_algorithm('AAPL', '1Min', 10)   