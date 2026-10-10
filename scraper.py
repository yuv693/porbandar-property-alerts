import time
import requests
from bs4 import BeautifulSoup

print("Porbandar Property Scraper Started Successfully!")

while True:
    try:
        # Yahan par IBAPI / Auction site scraping ka code aayega
        print("Checking for new Porbandar property auctions...")
    except Exception as e:
        print(f"Error: {e}")
    
    # Har 1 ghante mein check karega
    time.sleep(3600)
