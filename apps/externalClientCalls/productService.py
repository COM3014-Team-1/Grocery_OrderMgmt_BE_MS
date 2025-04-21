import requests
from flask import Flask, request, jsonify
from apps.utils.util import util
from flask import current_app


# PRODUCT_UPDATE_URL = current_app.config['PRODUCT_UPDATE_URL']

def check_product_availability_bulk(product_ids, auth_header):
    PRODUCT_SERVICE_URL = current_app.config["PRODUCT_SERVICE_URL"]
    headers = {
        "Authorization": auth_header,
        "Content-Type": "application/json"
    }
    current_app.logger.info("Headder: "+str(headers))
    current_app.logger.info("Sending request to Product Service to check product Avaliability:"+str(product_ids))
    response = requests.post(PRODUCT_SERVICE_URL, json={"product_ids": product_ids}, headers=headers)
    current_app.logger.info("Response from Product service: "+str(response))
    if response.status_code == 200:
        UnavaliableProducts=util.check_product_avalibility(response.json())
        current_app.logger.info("UnavaliableProducts: "+str(UnavaliableProducts))
        if UnavaliableProducts:
            return UnavaliableProducts
        return None
    else:
        return None