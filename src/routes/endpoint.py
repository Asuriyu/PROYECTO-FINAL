from enum import Enum
from src.config.config import BASE_URL


class Endpoint(Enum):

    LOGIN = "/api/v2/admin/administrators/token"

    BASE_TAXONS = "/api/v2/admin/taxons"
    BASE_TAXONS_CODE = "/api/v2/admin/taxons/{code}"

    BASE_ADMINS = "/api/v2/admin/administrators"
    BASE_ADMINS_CODE = "/api/v2/admin/administrators/{id}"

    @classmethod
    def login(cls):
        return f"{BASE_URL}{cls.LOGIN.value}"