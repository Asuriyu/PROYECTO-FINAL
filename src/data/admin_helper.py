from src.services.request import SyliusRequest
from src.routes.administrators_endpoint import AdministratorsEndpoint
from src.assertions.status_code_assertion import AssertionStatusCode
from src.resources.payloads.administrators_payload import AdministratorsPayload
from src.data.administrators import generate_admin_data

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
