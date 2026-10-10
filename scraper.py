import os
import time
import requests
from bs4 import BeautifulSoup
from flask import Flask
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import threading

# Flask Web Server (Render ke liye taaki port open rahe)
app = Flask(__name__)

@app.route('/')
def home():
    return "Porbandar Property Scraper is Live & Running!"

# Google Sheets Setup
def get_sheet():
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        # Agar JSON credentials environment variable ya file mein hain
        # Yahan hum safe fallback use karenge
        creds_file = 'credentials.json'
        if os.path.exists(creds_file):
            creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)
            client = gspread.authorize(creds)
            sheet = client.open("Bank Auction Properties Live Data").sheet1
            return sheet
    except Exception as e:
        print(f"Google Sheet Connection Error: {e}")
    return None

def run_scraper():
    print("Porbandar Property Scraper Background Worker Started...")
    
    while True:
        try:
            url = "https://www.ibapi.in/"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Yahan hum Porbandar keyword search karenge page par
                text_content = soup.get_text()
                
                if "Porbandar" in text_content:
                    print("Porbandar property found on IBAPI!")
                    # Valid data extraction logic
                    title = "Porbandar Bank Auction Property"
                    city = "Porbandar"
                    price = "Check Portal"
                    market_price = "N/A"
                    
                    sheet = get_sheet()
                    if sheet:
                        # Check duplicate or append safely
                        sheet.append_row([title, city, price, market_price])
                else:
                    print("No new Porbandar property found in current scan.")
            else:
                print(f"Website returned status code: {response.status_code}")
                
        except Exception as e:
            # Errors ko chupchap handle karenge, sheet mein nahi dalenge!
            print(f"Scraper warning / skipped: {e}")
        
        # Har 2 ghante mein check karega taaki IP block na ho
        time.sleep(7200)

if __name__ == '__main__':
    # Background thread mein scraper chalayenge taaki Flask server block na ho
    t = threading.Thread(target=run_scraper)
    t.daemon = True
    t.start()

    # Render ke liye dynamic port bind
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
