from src.services.request import SyliusRequest
from src.routes.product_reviews_endpoint import ProductReviewsEndpoint
from src.utils.logger_helpers import log_request_response

class ProductReviewsCall:

    @staticmethod
    def get_all(headers):
        url = ProductReviewsEndpoint.reviews()
        response = SyliusRequest.get(url, headers)
        log_request_response("GET", url, response, headers=headers)
        return response

    @staticmethod
    def get_with_params(headers, page=None, items_per_page=None):
        params = {}
        if page is not None:
            params["page"] = page
        if items_per_page is not None:
            params["itemsPerPage"] = items_per_page

        url = ProductReviewsEndpoint.reviews_with_params(**params)
        response = SyliusRequest.get(url, headers)
        log_request_response("GET", url, response, headers=headers)
        return response

    @staticmethod
    def get_by_id(headers, review_id):
        url = ProductReviewsEndpoint.review_by_id(review_id)
        response = SyliusRequest.get(url, headers)
        log_request_response("GET", url, response, headers=headers)
        return response

    @staticmethod
    def delete(headers, review_id):
        url = ProductReviewsEndpoint.review_by_id(review_id)
        response = SyliusRequest.delete(url, headers)
        log_request_response("DELETE", url, response, headers=headers)
        return response