import os
import time
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Porbandar Property Scraper is Live & Running!"

if __name__ == '__main__':
    # Render ke liye dynamic port bind karna zaroori hai
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
