import requests
from flask import Flask, request, jsonify
from apps.utils.util import util
from flask import current_app
from apps.exception.exception import ProductAvailabilityError


class productservice:
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
    
    def update_product_qty(product_to_update,auth_header):
        try:
            PRODUCT_UPDATE_URL = current_app.config["PRODUCT_UPDATE_URL"]
            headers = {
                "Authorization": auth_header,
                "Content-Type": "application/json"
            }
            current_app.logger.info("Headder: "+str(headers))
            current_app.logger.info("Sending request to Product Service to updte product quantity:"+str(product_to_update))
            response = requests.put(PRODUCT_UPDATE_URL, json={"product_ids": product_to_update}, headers=headers)
            current_app.logger.info("Response from Product service: "+str(response.json()))
            if response.status_code == 200:
                current_app.logger.info("Updating products successful for products"+str(response.json))
                return None
            else:
                errUpdating=util.get_error_product_ids(response.json())
                if errUpdating:
                    current_app.logger.info("err Updating products as they are out of stock: "+str(errUpdating))
                    raise ProductAvailabilityError(errUpdating)
                else:
                    current_app.logger.info("err Updating products stock "+str(response.json))
                    raise Exception(response.json())
        except ProductAvailabilityError as err:
            current_app.logger.warning("product update failed due to unavailable products.")
            raise err
        except Exception as err:
            raise err