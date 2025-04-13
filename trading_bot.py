import ccxt
import time
import pandas as pd

# --- API Setup ---
api_key = 'YOUR_API_KEY'
api_secret = 'YOUR_API_SECRET'

exchange = ccxt.binance({
    'apiKey': api_key,
    'secret': api_secret,
    'enableRateLimit': True,
})

symbol = 'BTC/USDT'
timeframe = '1m'  # 1-minute candles
limit = 100  # Number of candles to fetch

# --- Trading Parameters ---
sma_short_period = 5
sma_long_period = 20
order_size = 0.001  # BTC to buy/sell

def fetch_data():
    """Fetch historical candle data."""
    candles = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    return df

def calculate_sma(df):
    """Calculate short and long moving averages."""
    df['SMA_Short'] = df['close'].rolling(sma_short_period).mean()
    df['SMA_Long'] = df['close'].rolling(sma_long_period).mean()
    return df

def place_order(order_type):
    """Place a buy or sell order."""
    try:
        if order_type == 'buy':
            print("Placing Buy Order...")
            exchange.create_market_buy_order(symbol, order_size)
        elif order_type == 'sell':
            print("Placing Sell Order...")
            exchange.create_market_sell_order(symbol, order_size)
    except Exception as e:
        print(f"Order Error: {e}")

def run_bot():
    """Main loop for the trading bot."""
    while True:
        df = fetch_data()
        df = calculate_sma(df)
        
        if df['SMA_Short'].iloc[-2] < df['SMA_Long'].iloc[-2] and df['SMA_Short'].iloc[-1] > df['SMA_Long'].iloc[-1]:
            place_order('buy')  # Golden cross
        elif df['SMA_Short'].iloc[-2] > df['SMA_Long'].iloc[-2] and df['SMA_Short'].iloc[-1] < df['SMA_Long'].iloc[-1]:
            place_order('sell')  # Death cross
        
        time.sleep(60)  # Wait for the next candle

if __name__ == '__main__':
    run_bot()
