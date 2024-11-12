from mongoengine import Document, StringField, DateTimeField, ListField, ReferenceField

class FinancialNews(Document):
    title = StringField(required=True)  # Title of the news article
    content = StringField()  # Full content of the article
    summary = StringField()  # Summary or short description
    published_date = DateTimeField(required=True)  # Publication date
    source = StringField()  # Source of the news article (e.g., Reuters, Bloomberg)
    tags = ListField(StringField())  # Tags or keywords related to the article
    related_symbols = ListField(StringField())  # Stocks mentioned in the article

    meta = {
        'indexes': [
            {'fields': ['published_date', 'title'], 'unique': True}  # Ensures uniqueness based on title and date
        ]
    }