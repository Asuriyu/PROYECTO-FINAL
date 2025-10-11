from src.routes.endpoint import Endpoint
from src.config.config import BASE_URL

class AdministratorsEndpoint:

    @classmethod
    def admins(cls):
        return f"{BASE_URL}{Endpoint.BASE_ADMINS.value}"
    
    @classmethod
    def admins_with_params(cls, **params):
        base_url = f"{BASE_URL}{Endpoint.BASE_ADMINS.value}"
        if params:
            query_string = "&".join([f"{key}={value}" for key, value in params.items()])
            return f"{base_url}?{query_string}"
        return base_url

    @classmethod
    def create_admin(cls):
        return cls.admins()
    
    @staticmethod
    def build_admin_code(base, admin_id):
        return f"{BASE_URL}{base.format(id=admin_id)}"
    
    @classmethod
    def admin_code(cls, admin_id):
        return f"{BASE_URL}{Endpoint.BASE_ADMINS_CODE.value.format(id=admin_id)}"