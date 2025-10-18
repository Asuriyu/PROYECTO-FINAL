import requests
import os
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
        return requests.get(full_url, headers=headers)

    @staticmethod
    def post(url, headers=None, payload=None, files=None):
        if headers is None:
            headers = {}
        full_url = SyliusRequest._full_url(url)
        if files:
            return requests.post(full_url, headers=headers, files=files, data=payload)
        headers = headers.copy()
        headers.update({'Content-Type': 'application/json'})
        return requests.post(full_url, headers=headers, json=payload)

    @staticmethod
    def put(url, headers, payload=None):
        full_url = SyliusRequest._full_url(url)
        headers = headers.copy()
        if 'content-type' not in {k.lower() for k in headers.keys()}:
            headers['Content-Type'] = 'application/json'
        return requests.put(full_url, headers=headers, json=payload)

    @staticmethod
    def put_with_custom_headers(url, headers, payload=None):
        full_url = SyliusRequest._full_url(url)
        headers = headers.copy()
        headers.update({'Content-Type': 'application/ld+json'})
        return requests.put(full_url, headers=headers, json=payload)

    @staticmethod
    def delete(url, headers, payload=None):
        full_url = SyliusRequest._full_url(url)
        headers = headers.copy()
        headers.update({'Content-Type': 'application/json'})
        return requests.delete(full_url, headers=headers, json=payload)

    @staticmethod
    def patch(url, headers=None, payload=None):
        full_url = SyliusRequest._full_url(url)
        headers = headers.copy() if headers else {}
        headers.update({'Content-Type': 'application/json'})
        return requests.patch(full_url, headers=headers, json=payload)