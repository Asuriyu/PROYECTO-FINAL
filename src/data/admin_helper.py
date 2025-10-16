from src.services.request import SyliusRequest
from src.routes.administrators_endpoint import AdministratorsEndpoint
from src.assertions.status_code_assertion import AssertionStatusCode
from src.resources.payloads.administrators_payload import AdministratorsPayload
from src.data.administrators import generate_admin_data

def get_avatar_url(admin_id: int) -> str:
    return f"{AdministratorsEndpoint.admins()}/{admin_id}/avatar-image"

def create_temp_admin(headers):
    """
    Crea un administrador temporal y retorna (admin_id, payload)
    """
    payload = AdministratorsPayload.build_payload_admin(generate_admin_data())
    url = AdministratorsEndpoint.admins()
    response = SyliusRequest.post(url, headers, payload)
    AssertionStatusCode.assert_status_code_201(response)
    return response.json()["id"], payload

def delete_temp_admin(headers, admin_id):
    """
    Elimina un administrador temporal creado para pruebas
    """
    url = f"{AdministratorsEndpoint.admins()}/{admin_id}"
    response = SyliusRequest.delete(url, headers)
    AssertionStatusCode.assert_status_code_204(response)

def disable_admin(headers, admin_id):
    url = f"{AdministratorsEndpoint.admins()}/{admin_id}"
    h = {**headers, "Content-Type": "application/merge-patch+json", "Accept": "application/json"}
    payload = {"enabled": False}
    response = SyliusRequest.patch(url, h, payload)
    AssertionStatusCode.assert_status_code_200(response)
    return response