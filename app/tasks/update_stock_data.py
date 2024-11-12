import os
import time
from datetime import datetime, timedelta
from app.services.stock_service import add_stock_data, get_latest_stock_data
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv()
API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
BASE_URL = "https://www.alphavantage.co/query"

def fetch_daily_data(symbol):
    """Fetch daily stock data from Alpha Vantage"""
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return data.get("Time Series (Daily)", {})
    else:
        print(f"Error fetching data for {symbol}: {response.status_code}")
        return {}

def update_stock_data(symbols):
    """Update stock data for a list of symbols"""
    for symbol in symbols:
        print(f"Updating data for {symbol}")
        daily_data = fetch_daily_data(symbol)
        
        latest_data = get_latest_stock_data(symbol)
        latest_date_in_db = latest_data['date'] if latest_data else None

        for date_str, values in daily_data.items():
            date = datetime.strptime(date_str, "%Y-%m-%d")
            
            # Skip dates that are already in the database
            if latest_date_in_db and date <= latest_date_in_db:
                continue

            open_price = float(values["1. open"])
            high = float(values["2. high"])
            low = float(values["3. low"])
            close = float(values["4. close"])
            volume = int(values["5. volume"])

            result = add_stock_data(
                symbol=symbol,
                date=date,
                open=open_price,
                close=close,
                high=high,
                low=low,
                volume=volume
            )
            print(f"Stored updated data for {symbol} on {date_str}: {result}")

