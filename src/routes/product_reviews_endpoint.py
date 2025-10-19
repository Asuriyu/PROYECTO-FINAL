from src.routes.endpoint import Endpoint
from src.config.config import BASE_URL

class ProductReviewsEndpoint:

    @classmethod
    def reviews(cls):
        return f"{BASE_URL}{Endpoint.BASE_PRODUCT_REVIEWS.value}"

    @classmethod
    def reviews_with_params(cls, **params):
        base_url = f"{BASE_URL}{Endpoint.BASE_PRODUCT_REVIEWS.value}"
        if params:
            query_string = "&".join([f"{key}={value}" for key, value in params.items()])
            return f"{base_url}?{query_string}"
        return base_url

    @classmethod
    def create_product_review(cls):
        return cls.product_reviews()

    @classmethod
    def product_review_id(cls, review_id: str):
        return f"{BASE_URL}{Endpoint.BASE_PRODUCT_REVIEW_ID.value.format(review_id=review_id)}"

    @classmethod
    def delete_product_review(cls, review_id: str):
        return cls.product_review_id(review_id)