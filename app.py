import signal
import sys
import logging
import warnings
import time
from flask import Flask, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Suppress SSL and other warnings
warnings.filterwarnings("ignore", category=UserWarning, module='selenium')
warnings.filterwarnings("ignore", category=ResourceWarning)
warnings.filterwarnings("ignore", message=".*SSL.*")
logging.getLogger('urllib3').setLevel(logging.CRITICAL)
logging.getLogger('selenium').setLevel(logging.CRITICAL)

logging.basicConfig(level=logging.ERROR)

app = Flask(__name__)
CORS(app)

def shutdown(signal, frame):
    print("Shutting down gracefully...")
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

def fetch_items(driver, page_number):
    url = f'https://traderie.com/royalehigh/products?page={page_number}'
    
    items = []
    print(f"Attempting to fetch page {page_number}")
    
    try:
        driver.get(url)
        
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'sc-eqUAAy.sc-SrznA.cZMYZT.WYSac.item-img-container'))
        )

        print(f"Page {page_number} loaded")
        
        no_results_message = driver.find_elements(By.CLASS_NAME, 'no-items')
        if no_results_message and "No results could be found" in no_results_message[0].text:
            print(f"No results on page {page_number}")
            return None
        
        item_containers = driver.find_elements(By.CLASS_NAME, 'sc-eqUAAy.sc-SrznA.cZMYZT.WYSac.item-img-container')
        if not item_containers:
            print(f"No item containers found on page {page_number}")
        else:
            for container in item_containers:
                try:
                    name_container = container.find_element(By.CLASS_NAME, 'sc-czkgLR.fsFCnf')
                    item_name = name_container.text
                except:
                    item_name = "Unknown"
                try:
                    value_container = container.find_element(By.CLASS_NAME, 'listing-bells')
                    item_value = int(value_container.text.replace(',', ''))
                except:
                    item_value = 0
                items.append({"name": item_name, "value": item_value})

        print(f"Page {page_number}: Found {len(items)} items")

    except Exception as e:
        print(f"Error on page {page_number}: {e}")
        return None

    return items

@app.route('/items', methods=['GET'])
def get_items():
    all_items = []
    page_number = 0
    start_time = time.time()
    
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--allow-insecure-localhost")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")
    chrome_options.add_argument("--disable-extensions")
    custom_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    chrome_options.add_argument(f'user-agent={custom_user_agent}')
    
    with webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=chrome_options
    ) as driver:
        while True:
            batch_items = []
            for _ in range(5):
                items = fetch_items(driver, page_number)
                if items is None:
                    break
                batch_items.extend(items)
                page_number += 1

            if not batch_items:
                print(f"No more data starting from page {page_number}. Stopping.")
                break

            all_items.extend(batch_items)
    
    elapsed_time = time.time() - start_time
    print(f"Scraped {len(all_items)} items in {elapsed_time:.2f} seconds")
    
    return jsonify(all_items)

if __name__ == '__main__':
    app.run(debug=True)
