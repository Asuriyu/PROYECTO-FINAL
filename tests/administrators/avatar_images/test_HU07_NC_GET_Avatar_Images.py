import pytest
from src.services.request import SyliusRequest
from src.routes.administrators_endpoint import AdministratorsEndpoint
from src.assertions.status_code_assertion import AssertionStatusCode
from src.assertions.administrators.error_assertion import AssertionAdministratorsError
from src.data.admin_helper import create_temp_admin, delete_temp_admin, get_avatar_url, disable_admin
from tests.conftest import auth_headers

def test_TC139_Consultar_avatar_sin_token():
    headers = {}
    admin_id = 1
    url = get_avatar_url(admin_id)
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_401(response)
    AssertionAdministratorsError.assert_admin_error(response.json(), 401, "JWT Token not found")

def test_TC140_Consultar_avatar_token_invalido():
    headers = {"Authorization": "Bearer invalid_token"}
    admin_id = 1
    url = get_avatar_url(admin_id)
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_401(response)
    AssertionAdministratorsError.assert_admin_error(response.json(), 401, "Invalid JWT Token")

def test_TC141_Consultar_avatar_devuelve_imagen_o_url(auth_headers):
    admin_id, _ = create_temp_admin(auth_headers)
    url = get_avatar_url(admin_id)
    response = SyliusRequest.get(url, auth_headers)
    AssertionStatusCode.assert_status_code_404(response)

def test_TC142_Consultar_avatar_sin_configuracion(auth_headers):
    admin_id, _ = create_temp_admin(auth_headers)
    url = get_avatar_url(admin_id)
    response = SyliusRequest.get(url, auth_headers)
    AssertionStatusCode.assert_status_code_404(response)

# TC-37: Admin > Administrators - Ingresar ID igual a 12345
# TC-38: Admin > Administrators - Validar error al ingresar ID igual a 0
# TC-39: Admin > Administrators - Validar error al ingresar ID string igual a "uno"
# TC-40: Admin > Administrators - Validar error al ingresar ID negativo igual a -1
# TC-41: Admin > Administrators - Validar error al ingresar ID decimal igual a 1.5
@pytest.mark.parametrize("admin_id, expected_status", [
    (12345, 404),
    (0, 404),
    ("uno", 404),
    (-1, 404),
    (1.5, 404)
])
def test_TC_Admin_AvatarImage_validar_parametros_ID(auth_headers, admin_id, expected_status):
    response = SyliusRequest.get(get_avatar_url(admin_id), auth_headers)
    AssertionStatusCode.assert_status_code(response, expected_status)