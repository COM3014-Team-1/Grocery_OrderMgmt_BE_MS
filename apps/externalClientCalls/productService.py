import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

PRODUCT_SERVICE_URL = app.config['PRODUCT_SERVICE_URL']
PRODUCT_UPDATE_URL = app.config['PRODUCT_UPDATE_URL']

def check_product_availability_bulk(product_ids):
    response = requests.post(PRODUCT_SERVICE_URL, json={"product_ids": product_ids})
    
    if response.status_code == 200:
        return response.json()
    else:
        return None