import requests
from src.utils.logger_helpers import log_request_response
import time
import logging

def safe_request(method, url, retries=3, delay=2, **kwargs):
    for attempt in range(1, retries + 1):
        try:
            response = requests.request(method, url, **kwargs)
            log_request_response(method, url, response, kwargs.get("headers"), kwargs.get("json"))
            return response
        except requests.exceptions.ConnectionError as e:
            logging.warning(f"Intento {attempt}/{retries} fallido por conexión: {e}")
            if attempt < retries:
                time.sleep(delay)
            else:
                raise