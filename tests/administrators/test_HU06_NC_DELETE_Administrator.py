import pytest
import allure
from src.services.request import SyliusRequest
from src.routes.administrators_endpoint import AdministratorsEndpoint
from src.assertions.status_code_assertion import AssertionStatusCode
from src.assertions.administrators.error_assertion import AssertionAdministratorsError
from src.data.administrators import generate_admin_data
from src.resources.payloads.administrators_payload import AdministratorsPayload
from src.utils.admin_helper import create_temp_admin

# TC-131: Admin > Administrators – Eliminar administrador existente con ID válido
@allure.epic("Módulo de Administrador")
@allure.feature("Administrators")
@allure.story("Eliminar administrador")
@allure.title("SYLIUS-131: Eliminar administrador existente con ID válido")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.administrator
@pytest.mark.functional_positive
@pytest.mark.high
def test_TC131_Eliminar_administrador_existente_con_id_valido(auth_headers):
    headers = auth_headers
    admin_id, _ = create_temp_admin(headers)
    url = f"{AdministratorsEndpoint.admins()}/{admin_id}"
    response = SyliusRequest.delete(url, headers)
    AssertionStatusCode.assert_status_code_204(response)
    check = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_404(check)

# TC-132: Admin > Administrators – Validar error al eliminar administrador inexistente
@allure.epic("Módulo de Administrador")
@allure.feature("Administrators")
@allure.story("Eliminar administrador")
@allure.title("SYLIUS-132: Validar error al eliminar administrador inexistente")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.administrator
@pytest.mark.functional_negative
@pytest.mark.medium
def test_TC132_Eliminar_administrador_inexistente(auth_headers):
    headers = auth_headers
    nonexistent_id = "99999999"
    url = f"{AdministratorsEndpoint.admins()}/{nonexistent_id}"
    response = SyliusRequest.delete(url, headers)
    AssertionStatusCode.assert_status_code_404(response)
    AssertionAdministratorsError.assert_admin_error(response.json(), 404, "Administrator not found")

# TC-133: Admin > Administrators – Validar error al eliminar administrador sin token de autenticación
@allure.epic("Módulo de Administrador")
@allure.feature("Administrators")
@allure.story("Eliminar administrador")
@allure.title("SYLIUS-133: Validar error al eliminar administrador sin token de autenticación")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.administrator
@pytest.mark.security
@pytest.mark.functional_negative
@pytest.mark.high
def test_TC133_Eliminar_administrador_sin_token():
    headers = {}
    admin_id = "12345"
    url = f"{AdministratorsEndpoint.admins()}/{admin_id}"
    response = SyliusRequest.delete(url, headers)
    AssertionStatusCode.assert_status_code_401(response)
    AssertionAdministratorsError.assert_admin_error(response.json(), 401, "JWT Token not found")

# TC-134: Admin > Administrators – Validar error al eliminar administrador con token inválido
@allure.epic("Módulo de Administrador")
@allure.feature("Administrators")
@allure.story("Eliminar administrador")
@allure.title("SYLIUS-134: Validar error al eliminar administrador con token inválido")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.administrator
@pytest.mark.security
@pytest.mark.functional_negative
@pytest.mark.high
def test_TC134_Eliminar_administrador_token_invalido():
    headers = {"Authorization": "Bearer invalid_token"}
    admin_id = "12345"
    url = f"{AdministratorsEndpoint.admins()}/{admin_id}"
    response = SyliusRequest.delete(url, headers)
    AssertionStatusCode.assert_status_code_401(response)
    AssertionAdministratorsError.assert_admin_error(response.json(), 401, "Invalid JWT Token")

# TC-135: Admin > Administrators – Verificar eliminación de administrador deshabilitado
@allure.epic("Módulo de Administrador")
@allure.feature("Administrators")
@allure.story("Eliminar administrador")
@allure.title("SYLIUS-135: Verificar eliminación de administrador deshabilitado")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.administrator
@pytest.mark.functional_positive
@pytest.mark.medium
def test_TC135_Eliminar_administrador_deshabilitado(auth_headers):
    headers = auth_headers
    admin_data = generate_admin_data()
    admin_data["enabled"] = False
    payload = AdministratorsPayload.build_payload_admin(admin_data)
    url_create = AdministratorsEndpoint.admins()
    response_create = SyliusRequest.post(url_create, headers, payload)
    AssertionStatusCode.assert_status_code_201(response_create)
    admin_id = response_create.json()["id"]
    url_delete = f"{AdministratorsEndpoint.admins()}/{admin_id}"
    response_delete = SyliusRequest.delete(url_delete, headers)
    AssertionStatusCode.assert_status_code_204(response_delete)

# TC-136: Admin > Administrators – Validar error al eliminar administrador repetido
@allure.epic("Módulo de Administrador")
@allure.feature("Administrators")
@allure.story("Eliminar administrador")
@allure.title("SYLIUS-136: Validar error al eliminar administrador repetido")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.administrator
@pytest.mark.functional_negative
@pytest.mark.functional_edgecase
@pytest.mark.medium
def test_TC136_Eliminar_administrador_repetido(auth_headers):
    headers = auth_headers
    admin_id, _ = create_temp_admin(headers)
    url = f"{AdministratorsEndpoint.admins()}/{admin_id}"
    response1 = SyliusRequest.delete(url, headers)
    AssertionStatusCode.assert_status_code_204(response1)
    response2 = SyliusRequest.delete(url, headers)
    AssertionStatusCode.assert_status_code_404(response2)
    AssertionAdministratorsError.assert_admin_error(response2.json(), 404, "Administrator not found")

# TC-137: Admin > Administrators – Verificar eliminación concurrente
@allure.epic("Módulo de Administrador")
@allure.feature("Administrators")
@allure.story("Eliminar administrador")
@allure.title("SYLIUS-137: Verificar eliminación concurrente")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.administrator
@pytest.mark.functional_negative
@pytest.mark.functional_edgecase
@pytest.mark.concurrent
@pytest.mark.medium
def test_TC137_Eliminar_administrador_concurrente(auth_headers):
    headers = auth_headers
    admin_id, _ = create_temp_admin(headers)
    url = f"{AdministratorsEndpoint.admins()}/{admin_id}"
    response1 = SyliusRequest.delete(url, headers)
    response2 = SyliusRequest.delete(url, headers)
    assert response1.status_code in [204, 404]
    assert response2.status_code in [204, 404]
    
# TC-138: Admin > Administrators – Verificar que un administrador eliminado no exista más
@allure.epic("Módulo de Administrador")
@allure.feature("Administrators")
@allure.story("Eliminar administrador")
@allure.title("SYLIUS-138: Verificar que un administrador eliminado no exista más")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.administrator
@pytest.mark.functional_positive
@pytest.mark.high
def test_TC138_Verificar_administrador_eliminado_no_exista(auth_headers):
    headers = auth_headers
    admin_id, _ = create_temp_admin(headers)
    delete_url = f"{AdministratorsEndpoint.admins()}/{admin_id}"
    response_delete = SyliusRequest.delete(delete_url, headers)
    AssertionStatusCode.assert_status_code_204(response_delete)
    get_url = f"{AdministratorsEndpoint.admins()}/{admin_id}"
    response_get = SyliusRequest.get(get_url, headers)
    AssertionStatusCode.assert_status_code_404(response_get)