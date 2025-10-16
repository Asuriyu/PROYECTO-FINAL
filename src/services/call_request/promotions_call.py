from src.services.request import SyliusRequest
from src.routes.promotions_endpoint import PromotionsEndpoint

class PromotionsCall:

    @staticmethod
    def create(headers, payload):
        """Crea una promoción (POST)."""
        url = PromotionsEndpoint.create_promotion()
        response = SyliusRequest.post(url, headers, payload)
        return response.json()

    @staticmethod
    def get_all(headers):
        """Obtiene todas las promociones (GET)."""
        url = PromotionsEndpoint.promotions()
        response = SyliusRequest.get(url, headers)
        return response.json()

    @staticmethod
    def get_by_code(headers, code):
        """Obtiene una promoción específica (GET /{code})."""
        url = PromotionsEndpoint.promotion_code(code)
        response = SyliusRequest.get(url, headers)
        return response.json()

    @staticmethod
    def update(headers, code, payload):
        """Actualiza una promoción existente (PUT /{code})."""
        url = PromotionsEndpoint.update_promotion(code)
        response = SyliusRequest.put(url, headers, payload)
        return response.json()

    @staticmethod
    def archive(headers, code):
        """Archiva una promoción (PATCH /{code}/archive)."""
        url = PromotionsEndpoint.archive_promotion(code)
        response = SyliusRequest.patch(url, headers)
        return response.json()

    @staticmethod
    def restore(headers, code):
        """Restaura una promoción archivada (PATCH /{code}/restore)."""
        url = PromotionsEndpoint.restore_promotion(code)
        response = SyliusRequest.patch(url, headers)
        return response.json()

    @staticmethod
    def delete(headers, code):
        """Elimina una promoción (DELETE /{code})."""
        url = PromotionsEndpoint.delete_promotion(code)
        response = SyliusRequest.delete(url, headers)
        return response.json()