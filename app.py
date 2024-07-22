from flask import Flask, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def fetch_items_from_page(page_number):
    url = f'https://traderie.com/royalehigh/products?page={page_number}'
    
    # Configure Selenium to use Chrome in headless mode with a custom user agent
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    custom_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    chrome_options.add_argument(f'user-agent={custom_user_agent}')
    
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    
    driver.get(url)
    
    # Wait for content to load, you might need to adjust the wait time or method
    driver.implicitly_wait(10)
    
    # Debugging: print the page source
    print(driver.page_source)
    
    # Find elements that match your criteria
    item_containers = driver.find_elements(By.CLASS_NAME, 'sc-eqUAAy.sc-SrznA.cZMYZT.WYSac.item-img-container')
    
    if not item_containers:
        print("No item containers found on this page.")
    
    items = []
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
    
    driver.quit()
    return items

@app.route('/items', methods=['GET'])
def get_items():
    all_items = []
    page_number = 0
    while True:
        items = fetch_items_from_page(page_number)
        if not items:
            break
        all_items.extend(items)
        page_number += 1
    
    return jsonify(all_items)

if __name__ == '__main__':
    app.run(debug=True)
