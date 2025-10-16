from src.routes.endpoint import Endpoint
from src.config.config import BASE_URL

class PromotionsEndpoint:

    @classmethod
    def promotions(cls):
        return f"{BASE_URL}{Endpoint.BASE_PROMOTIONS.value}"

    @classmethod
    def promotions_with_params(cls, **params):
        base_url = f"{BASE_URL}{Endpoint.BASE_PROMOTIONS.value}"
        if params:
            query_string = "&".join([f"{key}={value}" for key, value in params.items()])
            return f"{base_url}?{query_string}"
        return base_url

    @classmethod
    def create_promotion(cls):
        return cls.promotions()

    @classmethod
    def promotion_code(cls, code: str):
        return f"{BASE_URL}{Endpoint.BASE_PROMOTIONS_CODE.value.format(code=code)}"

    @classmethod
    def update_promotion(cls, code: str):
        return f"{BASE_URL}{Endpoint.BASE_PROMOTIONS_CODE.value.format(code=code)}"

    @classmethod
    def delete_promotion(cls, code: str):
        return f"{BASE_URL}{Endpoint.BASE_PROMOTIONS_CODE.value.format(code=code)}"

    @classmethod
    def archive_promotion(cls, code: str):
        return f"{BASE_URL}/api/v2/admin/promotions/{code}/archive"

    @classmethod
    def restore_promotion(cls, code: str):
        return f"{BASE_URL}/api/v2/admin/promotions/{code}/restore"