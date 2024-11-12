import os
import sys
# 将项目根目录添加到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
print(sys.path)
import time
import requests
from datetime import datetime
from mongoengine import connect
from app.services.stock_service import add_stock_data, get_latest_stock_data
from dotenv import load_dotenv
import pandas as pd

# 加载 .env 文件中的环境变量
load_dotenv()

# 初始化 MongoDB 连接
connect(
    db=os.getenv("MONGO_DB_NAME"),
    host=os.getenv("MONGO_URI")
)

API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
BASE_URL = "https://www.alphavantage.co/query"
MAX_API_CALLS_PER_MINUTE = 5  # Alpha Vantage 免费账户的限制

def fetch_stock_data(symbol):
    """从 Alpha Vantage 获取每日股票数据"""
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

def store_stock_data(symbol):
    """检查并存储指定股票的每日新数据"""
    stock_data = fetch_stock_data(symbol)
    if not stock_data:
        print(f"No data available for {symbol}")
        return

    latest_data = get_latest_stock_data(symbol)
    latest_date_in_db = latest_data['date'] if latest_data else None

    for date_str, values in stock_data.items():
        date = datetime.strptime(date_str, "%Y-%m-%d")
        
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
        print(f"Stored data for {symbol} on {date_str}: {result}")

def get_sp500_symbols():
    """从 Wikipedia 获取 S&P 500 指数的股票代码列表"""
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    html = requests.get(url).content
    df = pd.read_html(html, header=0)[0]  # 获取页面上第一个表格
    symbols = df['Symbol'].tolist()
    return symbols

def store_all_sp500_data():
    """下载并存储 S&P 500 所有股票数据"""
    symbols = get_sp500_symbols()
    for i, symbol in enumerate(symbols):
        print(f"Fetching data for {symbol} ({i+1}/{len(symbols)})")
        store_stock_data(symbol)
        
        # 每次 API 请求后休眠以避免超过 API 限制
        time.sleep(60 / MAX_API_CALLS_PER_MINUTE)

if __name__ == "__main__":
    store_all_sp500_data()
