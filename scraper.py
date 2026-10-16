import json
import os
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

def fetch_new_auctions():
    # Yahan Porbandar / Gujarat Bank Auction portal scraping logic aayega
    # Sample dynamic payload simulation
    new_entries = []
    
    # Example logic: Agar koi naya item mila jo existing JSON me nahi hai
    # Toh array me append karega
    return new_entries

def main():
    existing_data = load_existing_data()
    existing_ids = {item.get('id') for item in existing_data}

    new_auctions = fetch_new_auctions()
    added_count = 0

    for item in new_auctions:
        if item.get('id') not in existing_ids:
            # Naya item sabse upar add hoga
            existing_data.insert(0, item)
            existing_ids.add(item.get('id'))
            added_count += 1

    if added_count > 0:
        save_data(existing_data)
        print(f"Successfully added {added_count} new bank auction properties!")
    else:
        print("No new properties found today. Existing data preserved.")

if __name__ == '__main__':
    main()
