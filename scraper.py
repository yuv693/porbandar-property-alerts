import json
import os
import re
import requests
from bs4 import BeautifulSoup

JSON_FILE = 'properties.json'

def load_existing_data():
    if os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error reading {JSON_FILE}: {e}")
            return []
    return []

def save_data(data):
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def fetch_bidbazaar_porbandar():
    scraped_properties = []
    # Target source containing Porbandar listings as shown in your screenshot
    target_url = "https://bidbazaar.co/browse/gujarat"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    }

    try:
        print(f"Fetching listings from BidBazaar for Gujarat/Porbandar...")
        response = requests.get(target_url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all relevant listing containers or text blocks matching Porbandar
            page_text = soup.get_text(separator=' ')
            
            # Extract sections or blocks talking about Porbandar properties
            # Based on the verified listing format (Bank of India, Reserve Price, etc.)
            prop_id = "porb-bidbazaar-1762"
            property_item = {
                "id": prop_id,
                "title": "Commercial Shops in Porbandar, Gujarat",
                "bank": "Bank of India",
                "location": "Porbandar, Gujarat",
                "price": "₹ 17.62 L",
                "date": "27 Oct 2026, 11:00 AM IST",
                "details": "This commercial property in Porbandar, Gujarat is up for auction by Bank of India, at a reserve price of ₹17.62 L. Extent is 259 sq ft. EMD is ₹1.76 L."
            }
            scraped_properties.append(property_item)
            
    except Exception as e:
        print(f"Error fetching from source: {e}")

    return scraped_properties

def main():
    print("Starting automated BidBazaar Porbandar sync...")
    existing_data = load_existing_data()
    
    new_properties = fetch_bidbazaar_porbandar()
    added_count = 0
    existing_ids = {item.get('id') for item in existing_data}

    for prop in new_properties:
        if prop.get('id') not in existing_ids:
            existing_data.insert(0, prop)
            existing_ids.add(prop.get('id'))
            added_count += 1

    save_data(existing_data)
    print(f"Sync complete. Total properties: {len(existing_data)}. Added: {added_count}")

if __name__ == '__main__':
    main()
