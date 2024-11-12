from mongoengine import Document, StringField, FloatField, DateTimeField

class ExchangeRate(Document):
    base_currency = StringField(required=True)  # Base currency (e.g., USD)
    target_currency = StringField(required=True)  # Target currency (e.g., EUR)
    rate = FloatField(required=True)  # Exchange rate at the specific date
    date = DateTimeField(required=True)  # Date of the exchange rate

    meta = {
        'indexes': [
            {'fields': ['base_currency', 'target_currency', 'date'], 'unique': True}  # Unique index for date and currency pair
        ]
    }