from src.routes.endpoint import Endpoint
from src.config.config import BASE_URL

class PromotionsEndpoint:

    @classmethod
    def promotions(cls):
        """Obtiene la colección de promociones"""
        return f"{BASE_URL}{Endpoint.BASE_PROMOTIONS.value}"

    @classmethod
    def promotions_with_params(cls, **params):
        """Obtiene la colección de promociones con parámetros (paginación, filtros, etc.)"""
        base_url = f"{BASE_URL}{Endpoint.BASE_PROMOTIONS.value}"
        if params:
            query_string = "&".join([f"{key}={value}" for key, value in params.items()])
            return f"{base_url}?{query_string}"
        return base_url

    @classmethod
    def create_promotion(cls):
        """Crea una nueva promoción"""
        return cls.promotions()

    @classmethod
    def promotion_code(cls, code: str):
        """Obtiene o actualiza una promoción específica por code"""
        return f"{BASE_URL}{Endpoint.BASE_PROMOTIONS_CODE.value.format(code=code)}"

    @classmethod
    def update_promotion(cls, code: str):
        """Actualiza una promoción existente"""
        return f"{BASE_URL}{Endpoint.BASE_PROMOTIONS_CODE.value.format(code=code)}"

    @classmethod
    def delete_promotion(cls, code: str):
        """Elimina una promoción existente"""
        return f"{BASE_URL}{Endpoint.BASE_PROMOTIONS_CODE.value.format(code=code)}"

    @classmethod
    def archive_promotion(cls, code: str):
        """Archiva una promoción existente"""
        return f"{BASE_URL}/api/v2/admin/promotions/{code}/archive"

    @classmethod
    def restore_promotion(cls, code: str):
        """Restaura una promoción previamente archivada"""
        return f"{BASE_URL}/api/v2/admin/promotions/{code}/restore"