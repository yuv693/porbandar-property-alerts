import os
import time
import requests
from bs4 import BeautifulSoup
from flask import Flask
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return "Porbandar Property Scraper is Live & Active!"

def get_sheet():
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds_file = 'credentials.json'
        if os.path.exists(creds_file):
            creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)
            client = gspread.authorize(creds)
            return client.open("Bank Auction Properties Live Data").sheet1
    except Exception as e:
        print(f"Google Sheet Auth Error: {e}")
    return None

def fetch_porbandar_properties():
    print("Searching for Porbandar, Gujarat properties...")
    
    # Target URL & headers
    url = "https://www.ibapi.in/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=20)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Text check for Porbandar, Gujarat
            content = soup.get_text()
            if "Porbandar" in content or "porbandar" in content.lower():
                sheet = get_sheet()
                if sheet:
                    # Fetch existing entries to avoid duplicates
                    existing_records = sheet.get_all_values()
                    existing_titles = [row[0] for row in existing_records if len(row) > 0]

                    # Extracted Property Format
                    title = "Commercial/Residential Property in Porbandar"
                    city = "Porbandar, Gujarat"
                    price = "Check Bank Notice"
                    market_price = "Auction Basis"

                    # Avoid duplicate entry
                    if title not in existing_titles:
                        sheet.append_row([title, city, price, market_price])
                        print("New Porbandar property added to Google Sheet!")
            else:
                print("No active Porbandar property listings found in this scan.")
        else:
            print(f"Server Response Code: {response.status_code}")

    except Exception as e:
        print(f"Scraping Error: {e}")

def run_background_scraper():
    while True:
        fetch_porbandar_properties()
        # Scan every 1 hour (3600 seconds)
        time.sleep(3600)

if __name__ == '__main__':
    t = threading.Thread(target=run_background_scraper)
    t.daemon = True
    t.start()

    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
