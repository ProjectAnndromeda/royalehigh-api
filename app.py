from flask import Flask, jsonify
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

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