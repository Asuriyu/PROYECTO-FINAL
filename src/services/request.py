from src.utils.logger_helpers import setup_logger, log_request_response
import requests
import os

setup_logger()

class SyliusRequest:
    BASE_URL = os.getenv("BASE_URL", "https://demo.sylius.com")

    @staticmethod
    def _full_url(url: str) -> str:
        if url.startswith("http"):
            return url
        return f"{SyliusRequest.BASE_URL.rstrip('/')}{url}"

    @staticmethod
    def get(url, headers):
        full_url = SyliusRequest._full_url(url)
        response = requests.get(full_url, headers=headers)
        log_request_response("GET", full_url, response, headers)
        return response

    @staticmethod
    def post(url, headers=None, payload=None, files=None):
        headers = headers or {}
        full_url = SyliusRequest._full_url(url)

        if files:
            response = requests.post(full_url, headers=headers, files=files, data=payload)
        else:
            headers = headers.copy()
            headers.update({'Content-Type': 'application/json'})
            response = requests.post(full_url, headers=headers, json=payload)

        log_request_response("POST", full_url, response, headers, payload)
        return response

    @staticmethod
    def put(url, headers, payload=None):
        full_url = SyliusRequest._full_url(url)
        headers = headers.copy()
        if 'content-type' not in {k.lower() for k in headers.keys()}:
            headers['Content-Type'] = 'application/json'
        response = requests.put(full_url, headers=headers, json=payload)
        log_request_response("PUT", full_url, response, headers, payload)
        return response

    @staticmethod
    def put_with_custom_headers(url, headers, payload=None):
        full_url = SyliusRequest._full_url(url)
        headers = headers.copy()
        headers.update({'Content-Type': 'application/ld+json'})
        response = requests.put(full_url, headers=headers, json=payload)
        log_request_response("PUT (custom)", full_url, response, headers, payload)
        return response

    @staticmethod
    def delete(url, headers, payload=None):
        full_url = SyliusRequest._full_url(url)
        headers = headers.copy()
        headers.update({'Content-Type': 'application/json'})
        response = requests.delete(full_url, headers=headers, json=payload)
        log_request_response("DELETE", full_url, response, headers, payload)
        return response

    @staticmethod
    def patch(url, headers=None, payload=None):
        full_url = SyliusRequest._full_url(url)
        headers = headers.copy() if headers else {}
        headers.update({'Content-Type': 'application/json'})
        response = requests.patch(full_url, headers=headers, json=payload)
        log_request_response("PATCH", full_url, response, headers, payload)
        return response