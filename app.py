from flask import Flask, jsonify
from flask_caching import Cache
from apscheduler.schedulers.background import BackgroundScheduler
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
scheduler = BackgroundScheduler()

@cache.cached(timeout=600, key_prefix='items')
def fetch_items():
    all_items = []
    page_number = 0
    while True:
        items = fetch_items_from_page(page_number)
        if not items:
            break
        all_items.extend(items)
        page_number += 1
    return all_items

def fetch_items_from_page(page_number):
    url = f'https://traderie.com/royalehigh/products?page={page_number}'
    response = requests.get(url)
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    item_containers = soup.find_all(class_='sc-eqUAAy sc-SrznA cZMYZT WYSac item-img-container')
    
    items = []
    for container in item_containers:
        name_container = container.find(class_='sc-czkgLR fsFCnf')
        item_name = name_container.text if name_container else None
        value_containers = container.find_all(class_='listing-bells')
        item_value = int(value_containers[1].text.replace(',', '')) if len(value_containers) > 1 else None
        items.append({"name": item_name, "value": item_value})
    
    return items

@app.route('/items', methods=['GET'])
def get_items():
    items = fetch_items()
    return jsonify(items)

def update_data():
    fetch_items()

if __name__ == '__main__':
    scheduler.add_job(update_data, 'interval', hours=1)
    scheduler.start()
    app.run(debug=True)
