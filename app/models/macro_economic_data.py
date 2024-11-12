from mongoengine import Document, StringField, DateTimeField, FloatField

class MacroEconomicData(Document):
    indicator_name = StringField(required=True)  # Name of the economic indicator
    value = FloatField(required=True)  # Value of the indicator
    date = DateTimeField(required=True)  # Date for the data entry
    unit = StringField()  # Unit of the indicator (e.g., %, index value)

    meta = {
        'indexes': [
            {'fields': ['indicator_name', 'date'], 'unique': True}  # Prevent duplicate data entries
        ]
    }
