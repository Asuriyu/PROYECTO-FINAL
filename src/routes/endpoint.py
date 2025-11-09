from enum import Enum
from src.config.config import BASE_URL


class Endpoint(Enum):

    LOGIN = "/api/v2/admin/administrators/token"

    BASE_ADMINS = "/api/v2/admin/administrators"
    BASE_ADMINS_CODE = "/api/v2/admin/administrators/{id}"

    BASE_PROMOTIONS = "/api/v2/admin/promotions"
    BASE_PROMOTIONS_CODE = "/api/v2/admin/promotions/{code}"
    PROMOTION_ARCHIVE = "/api/v2/admin/promotions/{code}/archive"
    PROMOTION_RESTORE = "/api/v2/admin/promotions/{code}/restore"

    BASE_PRODUCT_REVIEWS = "/api/v2/admin/product-reviews"
    BASE_PRODUCT_REVIEWS_ID = "/api/v2/admin/product-reviews/{review_id}"

    @classmethod
    def login(cls):
        return f"{BASE_URL}{cls.LOGIN.value}"
    
LOGIN2 = f"{BASE_URL}{Endpoint.LOGIN.value}"
PROMOTIONS = f"{BASE_URL}{Endpoint.BASE_PROMOTIONS.value}"