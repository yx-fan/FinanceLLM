import os
import sys
# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import requests
import pandas as pd
from mongoengine import connect
from dotenv import load_dotenv
from app.models.company_profile import CompanyProfile
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Initialize MongoDB connection
connect(
    db=os.getenv("MONGO_DB_NAME"),
    host=os.getenv("MONGO_URI")
)

def fetch_sp500_company_profiles():
    """Fetch S&P 500 company profiles from Wikipedia"""
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    html = requests.get(url).content
    df = pd.read_html(html, header=0)[0]  # Get the first table on the page
    return df[['Symbol', 'Security', 'GICS Sector', 'GICS Sub-Industry', 'Headquarters Location']].to_dict(orient='records')

def initialize_company_profiles():
    """Initialize company profiles in the database"""
    profiles = fetch_sp500_company_profiles()
    for profile in profiles:
        symbol = profile['Symbol']
        name = profile['Security']
        sector = profile['GICS Sector']
        industry = profile['GICS Sub-Industry']
        headquarters = profile['Headquarters Location']

        # Check if the company profile already exists
        existing_profile = CompanyProfile.objects(symbol=symbol).first()
        if not existing_profile:
            # Create a new company profile
            new_profile = CompanyProfile(
                symbol=symbol,
                name=name,
                sector=sector,
                industry=industry,
                headquarters=headquarters,
                description=None,  # 可通过其他来源补充
                website=None       # 可通过其他来源补充
            )
            new_profile.save()
            print(f"Added new company profile: {symbol}")
        else:
            print(f"Company profile already exists for {symbol}, skipping.")

if __name__ == "__main__":
    initialize_company_profiles()
