from flask import Blueprint, jsonify, request, current_app
from app.services.data_service import fetch_stock_data
from app.services.data_service import update_sp500_data

api_blueprint = Blueprint("api", __name__)

@api_blueprint.route("/stock", methods=["GET"])
def get_stock_data():
    symbol = request.args.get("symbol", "AAPL")  # 默认获取 Apple 的股票数据
    period = request.args.get("period", "1mo")  # 默认获取最近 1 个月的数据
    interval = request.args.get("interval", "1d")  # 默认日间数据

    data = fetch_stock_data(symbol, period, interval)
    if data:
        return jsonify({"symbol": symbol, "data": data}), 200
    else:
        return jsonify({"error": "Failed to fetch stock data"}), 500

@api_blueprint.route("/update_sp500_data", methods=["POST"])
def update_sp500():
    """手动更新 S&P 500 数据和日度股票数据"""
    update_sp500_data(current_app.db)
    return jsonify({"message": "S&P 500 data updated successfully."}), 200