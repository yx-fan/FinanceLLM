from app import create_app

# 使用应用工厂模式创建 Flask 应用
app = create_app()

if __name__ == "__main__":
    # 启动应用，指定 host 和 port
    app.run(host="0.0.0.0", port=5000, debug=True)