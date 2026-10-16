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

def fetch_porbandar_auctions():
    scraped_properties = []
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    # Major public bank auction aggregator portals (covers SBI, BOB, PNB, HDFC, ICICI, etc.)
    target_urls = [
        "https://www.bankauctions.in/search/?q=porbandar",
        "https://foreclosureindia.com/bank-auction-properties-in-porbandar"
    ]

    for url in target_urls:
        try:
            print(f"Checking bank auction listings from: {url}")
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extracting auction card items
                cards = soup.find_all(['div', 'article'], class_=re.compile(r'(property|auction|item|card|listing)', re.I))
                
                for idx, card in enumerate(cards):
                    text_content = card.get_text(separator=' ', strip=True)
                    
                    if 'porbandar' in text_content.lower():
                        # Basic automated extraction
                        title_match = card.find(['h2', 'h3', 'h4', 'a'])
                        title = title_match.get_text(strip=True) if title_match else "Porbandar Bank Auction Property"
                        
                        prop_id = f"auto-porb-{hash(title) % 100000}"
                        
                        property_item = {
                            "id": prop_id,
                            "title": title[:80],
                            "bank": "Bank Auction (Automated Sync)",
                            "location": "Porbandar, Gujarat",
                            "price": "Contact Bank / See Notice",
                            "date": "Check Notice Details",
                            "details": text_content[:200] + "..."
                        }
                        scraped_properties.append(property_item)
                        
        except Exception as e:
            print(f"Could not fetch from {url}: {e}")

    return scraped_properties

def main():
    print("Starting automatic Porbandar multi-bank data sync...")
    existing_data = load_existing_data()
    existing_ids = {item.get('id') for item in existing_data}

    new_properties = fetch_porbandar_auctions()
    added_count = 0

    for prop in new_properties:
        if prop.get('id') not in existing_ids:
            existing_data.insert(0, prop)
            existing_ids.add(prop.get('id'))
            added_count += 1

    save_data(existing_data)
    print(f"Sync complete. Total properties: {len(existing_data)}. New added: {added_count}")

if __name__ == '__main__':
    main()
