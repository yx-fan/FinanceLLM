from app.models.stock_data import StockData
from datetime import datetime

def add_stock_data(symbol, date, open, close, high, low, volume, metadata=None):
    """Add stock data to the database"""
    try:
        stock_data = StockData(
            symbol=symbol,
            date=date,
            open=open,
            close=close,
            high=high,
            low=low,
            volume=volume,
            metadata=metadata
        )
        stock_data.save()
        return stock_data
    except Exception as e:
        return str(e)

def get_latest_stock_data(symbol):
    """Get the latest stock data for a given symbol"""
    latest_data = StockData.objects(symbol=symbol).order_by("-date").first()
    return latest_data.to_mongo() if latest_data else None