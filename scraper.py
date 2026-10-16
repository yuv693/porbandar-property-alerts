import json
import os
import re
import requests

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
    
    # Advanced headers to mimic real user browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    url = "https://www.bankauctions.in/search/?q=porbandar"

    try:
        print(f"Connecting to target portal for Porbandar...")
        response = requests.get(url, headers=headers, timeout=25)
        print(f"Status Code received: {response.status_code}")

        if response.status_code == 200:
            # Search for property blocks using regex patterns
            text_data = response.text
            matches = re.findall(r'(?i)(porbandar[^<>\n\r]{15,180})', text_data)
            
            for idx, match in enumerate(set(matches)):
                clean_txt = re.sub(r'\s+', ' ', match).strip()
                prop_id = f"porb-live-{abs(hash(clean_txt)) % 100000}"
                
                property_item = {
                    "id": prop_id,
                    "title": f"Auction Notice: {clean_txt[:70]}...",
                    "bank": "Scheduled Bank E-Auction",
                    "location": "Porbandar, Gujarat",
                    "price": "See Bank Official Notice",
                    "date": "Active Notice",
                    "details": clean_txt
                }
                scraped_properties.append(property_item)
                
    except Exception as e:
        print(f"Connection exception: {e}")

    return scraped_properties

def main():
    print("Starting automated Porbandar synchronization...")
    existing_data = load_existing_data()
    
    # Clean any old test records if present
    existing_data = [item for item in existing_data if not item.get('id', '').startswith('demo-')]

    new_properties = fetch_porbandar_auctions()
    added_count = 0
    existing_ids = {item.get('id') for item in existing_data}

    for prop in new_properties:
        if prop.get('id') not in existing_ids:
            existing_data.insert(0, prop)
            existing_ids.add(prop.get('id'))
            added_count += 1

    save_data(existing_data)
    print(f"Sync completed. Total properties stored: {len(existing_data)}. Newly added: {added_count}")

if __name__ == '__main__':
    main()
