from mongoengine import Document, StringField

class CompanyProfile(Document):
    symbol = StringField(required=True, unique=True)  # Stock symbol
    name = StringField(required=True)  # Full name of the company
    sector = StringField()  # Sector (e.g., Technology, Healthcare)
    industry = StringField()  # Industry (e.g., Software, Pharmaceuticals)
    description = StringField()  # Company description
    headquarters = StringField()  # Location of headquarters
    website = StringField()  # Official website URL