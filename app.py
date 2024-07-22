from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

def fetch_items_from_page(page_number):
    url = f'https://traderie.com/royalehigh/products?page={page_number}'
    
    # Configure Selenium to use Chrome in headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
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
