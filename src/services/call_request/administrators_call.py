from src.routes.administrators_endpoint import AdministratorsEndpoint
from src.services.request import SyliusRequest

class AdministratorsCall:

    @classmethod
    def view(cls, headers, admin_id):
        response = SyliusRequest.get(AdministratorsEndpoint.admin_code(admin_id), headers)
        return response.json()

    @classmethod
    def create(cls, headers, payload):
        response = SyliusRequest.post(AdministratorsEndpoint.create_admin(), headers, payload)
        return response.json()

    @classmethod
    def update(cls, headers, payload, admin_id):
        response = SyliusRequest.put(AdministratorsEndpoint.admin_code(admin_id), headers, payload)
        return response.json()

    @classmethod
    def delete(cls, headers, admin_id):
        response = SyliusRequest().delete(AdministratorsEndpoint.admin_code(admin_id), headers)
        return response