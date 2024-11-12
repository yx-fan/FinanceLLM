import pandas as pd
import requests

def get_sp500_symbols():
    """从 Wikipedia 获取 S&P 500 指数的股票代码列表"""
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    html = requests.get(url).content
    df = pd.read_html(html, header=0)[0]  # 获取页面上第一个表格
    symbols = df['Symbol'].tolist()
    return symbols

# 示例：打印 S&P 500 股票代码列表
if __name__ == "__main__":
    sp500_symbols = get_sp500_symbols()
    print(f"Total S&P 500 symbols: {len(sp500_symbols)}")
    print(sp500_symbols)
