import requests
import os
import time
import json
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

#store name and API version
shop_url = "https://quickstart-bde7c873.myshopify.com"
api_version = "2023-07"

def get_all_products(shop_url, api_version):
    all_products = []
    url = f"{shop_url}/admin/api/{api_version}/products.json"
    headers = {"X-Shopify-Access-Token": os.getenv("SHOPIFY_API_KEY")}
    params = {"limit": 250}
    response = requests.get(url, headers=headers, params=params)
    all_products.extend(response.json()["products"])
    save_json(response.json())
    try:
        while response.links["next"]:
            response = requests.get(response.links["next"]["url"], headers=headers)
            all_products.extend(response.json()["products"])
            time.sleep(2)
    except KeyError:
        return all_products

def save_json(data):
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

all_products = get_all_products(shop_url, api_version)