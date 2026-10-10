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
    return "Multi-Bank Porbandar Auction Scraper is Active!"

def get_sheet():
    try:
        scope = ["https://spreadsheets.google.com/spreadsheets/v4/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds_file = 'credentials.json'
        if os.path.exists(creds_file):
            creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)
            client = gspread.authorize(creds)
            return client.open("Bank Auction Properties Live Data").sheet1
    except Exception as e:
        print(f"Google Sheet Connection Error: {e}")
    return None

def scan_bank_portals():
    print("Starting scan across official bank auction portals...")
    
    # List of bank property auction URLs & portals
    sources = [
        {"name": "IBAPI Portal", "url": "https://www.ibapi.in/"},
        {"name": "SBI e-Auction", "url": "https://sbi.co.in/web/sbi-in-the-news/auction-notices"},
        {"name": "Bank of Baroda SARFAESI", "url": "https://www.bankofbaroda.in/e-auction"},
        {"name": "PNB Auction Notices", "url": "https://www.pnbindia.in/e-auction.html"}
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }

    sheet = get_sheet()
    if not sheet:
        print("Sheet not reachable currently.")
        return

    existing_records = []
    try:
        existing_records = sheet.get_all_values()
    except Exception as e:
        print(f"Error fetching sheet records: {e}")

    existing_titles = [row[0] for row in existing_records if len(row) > 0]

    for source in sources:
        try:
            print(f"Scanning {source['name']}...")
            res = requests.get(source['url'], headers=headers, timeout=15)
            if res.status_code == 200:
                content = res.text.lower()
                if "porbandar" in content:
                    print(f"Found Porbandar listing on {source['name']}!")
                    
                    title = f"Bank Property Auction ({source['name']})"
                    city = "Porbandar, Gujarat"
                    price = "Check Bank Notice"
                    market_price = "Auction Basis"

                    if title not in existing_titles:
                        sheet.append_row([title, city, price, market_price])
                        existing_titles.append(title)
                        print(f"Added {title} to Google Sheet!")
            else:
                print(f"{source['name']} returned HTTP {res.status_code}")
        except Exception as e:
            print(f"Skipping {source['name']} due to connection timeout or block: {e}")

def run_background_loop():
    while True:
        scan_bank_portals()
        # Scan every 1 hour
        time.sleep(3600)

if __name__ == '__main__':
    t = threading.Thread(target=run_background_loop)
    t.daemon = True
    t.start()

    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
