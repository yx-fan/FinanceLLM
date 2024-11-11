from yahooquery import Ticker
from flask import current_app
import pandas as pd
from datetime import datetime, timedelta
import json

def update_sp500_list(db):
    """从 Wikipedia 获取最新的 S&P 500 成分股列表并存入 MongoDB"""
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    try:
        # 从 Wikipedia 获取 S&P 500 成分股列表
        tables = pd.read_html(url)
        sp500_table = tables[0]  # 第一张表通常是成分股列表
        sp500_symbols = sp500_table['Symbol'].tolist()

        # 清空旧的 S&P 500 列表
        db.sp500.delete_many({})
        
        # 插入新的 S&P 500 成分股列表
        db.sp500.insert_many([{"symbol": symbol, "is_sp500": True} for symbol in sp500_symbols])
        print("S&P 500 list updated in MongoDB.")
        
        return sp500_symbols
    except Exception as e:
        print(f"Failed to fetch S&P 500 list: {e}")
        return []

def fetch_and_save_daily_data(symbols, db):
    """使用 yahooquery 获取每支股票的最新日度数据并保存到 MongoDB"""
    try:
        ticker = Ticker(symbols)  # 获取多个股票的数据
        data = ticker.history(start=datetime.now() - timedelta(days=1), end=datetime.now(), interval="1d")

        # 检查返回的数据结构
        if isinstance(data, pd.DataFrame) and not data.empty:
            for symbol in symbols:
                if symbol in data.index.get_level_values(0):
                    stock_data = data.xs(symbol, level=0).reset_index()  # 提取特定股票的数据
                    stock_data["symbol"] = symbol
                    stock_data["is_sp500"] = True
                    stock_data["date"] = stock_data["date"].astype(str)  # 转换日期为字符串
                    records = json.loads(stock_data.to_json(orient="records"))

                    # 将数据插入到 daily_prices 集合中
                    db.daily_prices.insert_many(records)
                    print(f"Daily data for {symbol} saved to MongoDB.")
        else:
            print("No data retrieved from yahooquery.")
    except Exception as e:
        print(f"Failed to fetch daily data: {e}")

def update_sp500_data(db):
    # 更新 S&P 500 成分股列表
    sp500_symbols = update_sp500_list(db)
    
    # 获取并保存这些成分股的日度数据
    fetch_and_save_daily_data(sp500_symbols, db)

def fetch_stock_data(symbol, period="1mo", interval="1d"):
    """
    使用 yahooquery 获取单只股票的历史数据
    
    :param symbol: 股票代码
    :param period: 数据时间范围
    :param interval: 数据间隔
    """
    try:
        ticker = Ticker(symbol)
        data = ticker.history(period=period, interval=interval)

        if isinstance(data, pd.DataFrame) and not data.empty:
            data.reset_index(inplace=True)
            data["date"] = data["date"].astype(str)
            return data.to_dict(orient="records")
        else:
            print(f"No data retrieved for {symbol}")
            return None
    except Exception as e:
        current_app.logger.error(f"Failed to fetch stock data for {symbol}: {e}")
        return None
