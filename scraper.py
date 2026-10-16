import json
import os
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

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

def fetch_real_bank_auctions():
    scraped_properties = []
    target_url = "https://www.bankauctions.in/search/?q=porbandar"

    print("Launching headless browser to bypass security and fetch real data...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
        
        try:
            page.goto(target_url, timeout=40000)
            page.wait_for_timeout(5000) # Wait for JS to render content
            
            html_content = page.content()
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Find property cards or listing blocks
            cards = soup.find_all(['div', 'tr', 'li'], class_=lambda x: x and ('property' in x.lower() or 'auction' in x.lower() or 'item' in x.lower()))
            print(f"Found {len(cards)} elements on target page.")

            for card in cards:
                text_content = card.get_text(separator=' ', strip=True)
                if 'porbandar' in text_content.lower():
                    title_elem = card.find(['h2', 'h3', 'h4', 'a'])
                    title = title_elem.get_text(strip=True) if title_elem else "Bank e-Auction Property"
                    
                    prop_id = f"porb-real-{abs(hash(title)) % 100000}"
                    
                    property_item = {
                        "id": prop_id,
                        "title": title[:100],
                        "bank": "Scheduled Bank Portal",
                        "location": "Porbandar, Gujarat",
                        "price": "Check Official Bank Notice",
                        "date": "Live Auction",
                        "details": text_content[:250] + "..."
                    }
                    
                    if not any(p['id'] == prop_id for p in scraped_properties):
                        scraped_properties.append(property_item)
                        
        except Exception as e:
            print(f"Playwright navigation error: {e}")
        finally:
            browser.close()

    return scraped_properties

def main():
    print("Starting real automated sync for Porbandar...")
    existing_data = load_existing_data()
    
    # Clean any old test records if any
    existing_data = [item for item in existing_data if not item.get('id', '').startswith('demo-')]

    new_properties = fetch_real_bank_auctions()
    added_count = 0
    existing_ids = {item.get('id') for item in existing_data}

    for prop in new_properties:
        if prop.get('id') not in existing_ids:
            existing_data.insert(0, prop)
            existing_ids.add(prop.get('id'))
            added_count += 1

    save_data(existing_data)
    print(f"Sync complete. Total real properties: {len(existing_data)}. Newly added: {added_count}")

if __name__ == '__main__':
    main()
