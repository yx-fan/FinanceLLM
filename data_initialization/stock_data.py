import os
import sys
# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import time
import pandas as pd
import yfinance as yf
from datetime import datetime
from mongoengine import connect
from app.services.stock_service import add_stock_data, get_latest_stock_data
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv()

# Initialize MongoDB connection
connect(
    db=os.getenv("MONGO_DB_NAME"),
    host=os.getenv("MONGO_URI")
)

def fetch_historical_data_yfinance(symbol):
    """Fetch historical stock data using yfinance"""
    ticker = yf.Ticker(symbol)
    history = ticker.history(start="1990-01-01")  # Fetch data from 1990 onwards
    historical_data = []
    for date, row in history.iterrows():
        historical_data.append({
            "symbol": symbol,
            "date": date,
            "open": row["Open"],
            "high": row["High"],
            "low": row["Low"],
            "close": row["Close"],
            "volume": row["Volume"],
        })
    return historical_data

def store_historical_data(symbol):
    """Fetch and store historical stock data for a given symbol"""
    historical_data = fetch_historical_data_yfinance(symbol)
    for data in historical_data:
        # Check if the data already exists in the database
        existing_data = get_latest_stock_data(symbol)
        # Convert the date to a naive datetime object
        data_date_naive = data['date'].replace(tzinfo=None)
        
        if existing_data and existing_data['date'] >= data_date_naive:
            continue

        # Store the data in the database
        result = add_stock_data(
            symbol=data["symbol"],
            date=data["date"],
            open=data["open"],
            close=data["close"],
            high=data["high"],
            low=data["low"],
            volume=data["volume"]
        )
        print(f"Stored historical data for {symbol} on {data['date']}: {result}")

def get_sp500_symbols():
    """Get the list of S&P 500 symbols from Wikipedia"""
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    html = requests.get(url).content
    df = pd.read_html(html, header=0)[0]  # Get the first table on the page
    symbols = df['Symbol'].tolist()
    return symbols

def store_all_sp500_data():
    """Download and store historical data for all S&P 500 stocks"""
    symbols = get_sp500_symbols()
    for i, symbol in enumerate(symbols):
        print(f"Fetching historical data for {symbol} ({i+1}/{len(symbols)})")
        store_historical_data(symbol)
        
        # Pause for 1 second to avoid hitting the API rate limit
        time.sleep(1)

if __name__ == "__main__":
    store_all_sp500_data()
