from src.services.request import SyliusRequest
from src.routes.product_reviews_endpoint import ProductReviewsEndpoint
from src.utils.logger_helpers import log_request_response

class ProductReviewsCall:

    @staticmethod
    def create(headers, payload):
        url = ProductReviewsEndpoint.reviews()
        response = SyliusRequest.post(url, headers, payload)
        log_request_response("POST", url, headers=headers, payload=payload, response=response)
        return response

    @staticmethod
    def get_all(headers):
        url = ProductReviewsEndpoint.reviews()
        response = SyliusRequest.get(url, headers)
        log_request_response("GET", url, headers=headers, response=response)
        return response

    @staticmethod
    def get_by_id(headers, review_id):
        url = ProductReviewsEndpoint.product_review_id(review_id)
        response = SyliusRequest.get(url, headers)
        log_request_response("GET", url, headers=headers, response=response)
        return response

    @staticmethod
    def delete(headers, review_id):
        url = ProductReviewsEndpoint.product_review_id(review_id)
        response = SyliusRequest.delete(url, headers)
        log_request_response("DELETE", url, headers=headers, response=response)
        return response