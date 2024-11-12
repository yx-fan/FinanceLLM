from mongoengine import Document, StringField, FloatField, DateTimeField, BooleanField

class StockData(Document):
    symbol = StringField(required=True)  # Stock symbol (e.g., AAPL, MSFT)
    date = DateTimeField(required=True)  # Date of the data entry
    open = FloatField()  # Opening price
    close = FloatField()  # Closing price
    high = FloatField()  # Highest price
    low = FloatField()  # Lowest price
    volume = FloatField()  # Volume traded
    metadata = StringField()  # Any additional metadata

    meta = {
        'indexes': [
            {'fields': ['symbol', 'date'], 'unique': True}  # Unique index to prevent duplicate data
        ]
    }