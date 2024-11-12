from datetime import datetime
from mongoengine import Document, StringField, FloatField, DateTimeField

class SentimentAnalysis(Document):
    symbol = StringField(required=True)  # Stock symbol related to the analysis
    source = StringField()  # Source of the sentiment data (e.g., Twitter, News, Reddit)
    content = StringField()  # The content analyzed
    sentiment_score = FloatField()  # Sentiment score (positive, neutral, or negative)
    analysis_date = DateTimeField(default=datetime.now)  # Date of the analysis

    meta = {
        'indexes': [
            {'fields': ['symbol', 'analysis_date', 'source']}
        ]
    }