import pytest
from src.services.request import SyliusRequest
from src.routes.administrators_endpoint import AdministratorsEndpoint
from src.assertions.status_code_assertion import AssertionStatusCode
from src.assertions.administrators.error_assertion import AssertionAdministratorsError
from src.utils.admin_helper import create_temp_admin, get_avatar_url
from tests.conftest import auth_headers

# TC-139: Admin > Administrators > Avatar Images – Validar error al consultar imagen de avatar sin token de autenticación
def test_TC139_Validar_error_al_consultar_imagen_de_avatar_sin_token_de_autenticacion():
    headers = {}
    admin_id = 1
    url = get_avatar_url(admin_id)
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_401(response)
    AssertionAdministratorsError.assert_admin_error(response.json(), 401, "JWT Token not found")


# TC-140: Admin > Administrators > Avatar Images – Validar error al consultar avatar image con token inválido
def test_TC140_Validar_error_al_consultar_avatar_image_con_token_invalido():
    headers = {"Authorization": "Bearer invalid_token"}
    admin_id = 1
    url = get_avatar_url(admin_id)
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_401(response)
    AssertionAdministratorsError.assert_admin_error(response.json(), 401, "Invalid JWT Token")


# TC-141: Admin > Administrators > Avatar Images – Validar que path devuelva URL válida
def test_TC141_Validar_que_path_devuelva_URL_valida(auth_headers):
    admin_id, _ = create_temp_admin(auth_headers)
    url = get_avatar_url(admin_id)
    response = SyliusRequest.get(url, auth_headers)
    AssertionStatusCode.assert_status_code_404(response)


# TC-142: Admin > Administrators > Avatar Images – Verificar error cuando administrador no tiene avatar configurado
def test_TC142_Validar_error_al_consultar_avatar_sin_configuracion(auth_headers):
    admin_id, _ = create_temp_admin(auth_headers)
    url = get_avatar_url(admin_id)
    response = SyliusRequest.get(url, auth_headers)
    AssertionStatusCode.assert_status_code_404(response)


# TC-144: Admin > Administrators > Avatar Images - Ingresar ID igual a 12345
# TC-145: Admin > Administrators > Avatar Images - Validar error al ingresar ID igual a 0
# TC-146: Admin > Administrators > Avatar Images - Validar error al ingresar ID string igual a "uno"
# TC-147: Admin > Administrators > Avatar Images - Validar error al ingresar ID negativo igual a -1
# TC-148: Admin > Administrators > Avatar Images - Validar error al ingresar ID decimal igual a 1.5
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