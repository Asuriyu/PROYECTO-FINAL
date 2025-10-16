from src.services.request import SyliusRequest
from src.routes.promotions_endpoint import PromotionsEndpoint

class PromotionsCall:

    @staticmethod
    def create(headers, payload):
        url = PromotionsEndpoint.create_promotion()
        response = SyliusRequest.post(url, headers, payload)
        return response.json()

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
    def update(headers, code, payload):
        url = PromotionsEndpoint.update_promotion(code)
        response = SyliusRequest.put(url, headers, payload)
        return response.json()

    @staticmethod
    def archive(headers, code):
        url = PromotionsEndpoint.archive_promotion(code)
        response = SyliusRequest.patch(url, headers)
        return response.json()

    @staticmethod
    def restore(headers, code):
        url = PromotionsEndpoint.restore_promotion(code)
        response = SyliusRequest.patch(url, headers)
        return response.json()

    @staticmethod
    def delete(headers, promo_code):
        url = f"{PromotionsEndpoint.promotions()}/{promo_code}"
        response = SyliusRequest.delete(url, headers)
        if response.status_code == 204:
            return {"status": 204, "message": "Deleted successfully"}
        try:
            return response.json()
        except Exception:
            return {"status": response.status_code, "message": "No JSON content"}
