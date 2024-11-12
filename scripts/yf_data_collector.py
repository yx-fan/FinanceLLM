import os
import sys
# 将项目根目录添加到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import time
import pandas as pd
import yfinance as yf
from datetime import datetime
from mongoengine import connect
from app.services.stock_service import add_stock_data, get_latest_stock_data
from dotenv import load_dotenv
import requests

# 加载 .env 文件中的环境变量
load_dotenv()

# 初始化 MongoDB 连接
connect(
    db=os.getenv("MONGO_DB_NAME"),
    host=os.getenv("MONGO_URI")
)

def fetch_historical_data_yfinance(symbol):
    """从 Yahoo Finance 获取从 1990 年开始的历史数据"""
    ticker = yf.Ticker(symbol)
    history = ticker.history(start="1990-01-01")  # 设置开始日期为 1990 年 1 月 1 日
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
    """获取并存储完整的历史数据"""
    historical_data = fetch_historical_data_yfinance(symbol)
    for data in historical_data:
        # 检查数据是否已存在，避免重复插入
        existing_data = get_latest_stock_data(symbol)
        # 移除 data['date'] 的时区信息，以确保时间戳格式一致
        data_date_naive = data['date'].replace(tzinfo=None)
        
        if existing_data and existing_data['date'] >= data_date_naive:
            continue

        # 存储每个日期的数据
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
        print(f"Fetching historical data for {symbol} ({i+1}/{len(symbols)})")
        store_historical_data(symbol)
        
        # 为了防止 API 限制，每处理一只股票暂停 1 秒
        time.sleep(1)

if __name__ == "__main__":
    store_all_sp500_data()
