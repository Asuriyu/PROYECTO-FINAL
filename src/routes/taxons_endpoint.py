from src.routes.endpoint import Endpoint
from src.config.config import BASE_URL

class TaxonsEndpoint:

    @classmethod
    def taxon(cls):
        return f"{BASE_URL}{Endpoint.BASE_TAXONS.value}"
    
    @classmethod
    def taxons_with_params(cls, **params):
        base_url = f"{BASE_URL}{Endpoint.BASE_TAXONS.value}"
        if params:
            query_string = "&".join([f"{key}={value}" for key, value in params.items()])
            return f"{base_url}?{query_string}"
        return base_url
    
    @staticmethod
    def build_taxon_code(base, code):
        return f"{BASE_URL}{base.format(code=code)}"
    
    @classmethod
    def taxon_code(cls, code):
        return f"{BASE_URL}{Endpoint.BASE_TAXONS_CODE.value.format(code=code)}"