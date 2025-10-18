from src.services.request import SyliusRequest
from src.routes.promotions_endpoint import PromotionsEndpoint

class PromotionsCall:

    @staticmethod
    def create(headers, payload):
        url = PromotionsEndpoint.create_promotion()
        response = SyliusRequest.post(url, headers, payload)
        return response

    @staticmethod
    def get_all(headers):
        url = PromotionsEndpoint.promotions()
        response = SyliusRequest.get(url, headers)
        return response.json()

    @staticmethod
    def get_by_code(headers, code):
        url = PromotionsEndpoint.promotion_code(code)
        response = SyliusRequest.get(url, headers)
        return response.json()

    @staticmethod
    def update(headers, promo_code, payload):
        url = f"{PromotionsEndpoint.promotions()}/{promo_code}"
        response = SyliusRequest.put(url, headers, payload)
        return response
    
    @staticmethod
    def archive(headers, promo_code):
        url = f"{PromotionsEndpoint.promotions()}/{promo_code}/archive"
        response = SyliusRequest.patch(url, headers)
        return response

    @staticmethod
    def restore(headers, promo_code):
        url = f"{PromotionsEndpoint.promotions()}/{promo_code}/restore"
        response = SyliusRequest.patch(url, headers)
        return response

    @staticmethod
    def delete(headers, promo_code):
        url = f"{PromotionsEndpoint.promotions()}/{promo_code}"
        response = SyliusRequest.delete(url, headers)
        return response