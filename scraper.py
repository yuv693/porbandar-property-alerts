# Agar title ya price mein Error na ho, tabhi sheet mein row add karein
if title and "Error" not in title and "Exception" not in title and "Failed" not in title:
    sheet.append_row([title, city, price, market_price])
else:
    print("Invalid data, skipping...")
