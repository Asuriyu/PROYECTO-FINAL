import pytest
import io
import allure
from src.services.request import SyliusRequest
from src.routes.administrators_endpoint import AdministratorsEndpoint
from src.assertions.status_code_assertion import AssertionStatusCode
from src.assertions.administrators.schema_assertion import AssertionAdministrators
from src.assertions.administrators.error_assertion import AssertionAdministratorsError
from src.assertions.administrators.view_content_assertion import AssertionAdministratorsContent
from src.resources.payloads.administrators_payload import AdministratorsPayload
from src.data.administrators import generate_admin_data

# TC-175: Admin > Administrators > Avatar Images – Eliminar imagen de avatar existente con ID válido
@allure.epic("Módulo de Administrador")
@allure.feature("Administrators > Avatar Images")
@allure.story("Eliminar imagen de avatar")
@allure.title("SYLIUS-175: Eliminar imagen de avatar existente con ID válido")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.administrator
@pytest.mark.avatar_images
@pytest.mark.functional_positive
@pytest.mark.high
def test_TC175_Eliminar_avatar_existente_ID_valido(auth_headers, admin_id, sample_avatar_file):
    upload_url = AdministratorsEndpoint.avatar_upload(admin_id)
    delete_url = AdministratorsEndpoint.avatar_delete(admin_id)
    # Subir avatar primero
    SyliusRequest.post(upload_url, auth_headers, files=sample_avatar_file)
    # Luego eliminar
    response = SyliusRequest.delete(delete_url, auth_headers)
    AssertionStatusCode.assert_status_code_204(response)

# TC-176: Admin > Administrators > Avatar Images – Validar error al eliminar imagen de avatar inexistente
@allure.epic("Módulo de Administrador")
@allure.feature("Administrators > Avatar Images")
@allure.story("Eliminar imagen de avatar")
@allure.title("SYLIUS-176: Validar error al eliminar avatar inexistente")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.administrator
@pytest.mark.avatar_images
@pytest.mark.functional_negative
@pytest.mark.medium
def test_TC176_Error_eliminar_avatar_inexistente(auth_headers):
    url = AdministratorsEndpoint.avatar_delete(admin_id="99999")
    response = SyliusRequest.delete(url, auth_headers)
    AssertionStatusCode.assert_status_code_404(response)
    AssertionAdministratorsError.assert_avatar_not_found_error(response.json())

# TC-177: Admin > Administrators > Avatar Images – Validar error al eliminar avatar sin token de autenticación
@allure.epic("Módulo de Administrador")
@allure.feature("Administrators > Avatar Images")
@allure.story("Eliminar imagen de avatar")
@allure.title("SYLIUS-177: Validar error al eliminar avatar sin token de autenticación")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.administrator
@pytest.mark.avatar_images
@pytest.mark.security
@pytest.mark.functional_negative
@pytest.mark.high
def test_TC177_Error_eliminar_avatar_sin_token(admin_id):
    url = AdministratorsEndpoint.avatar_delete(admin_id)
    response = SyliusRequest.delete(url, headers={})
    AssertionStatusCode.assert_status_code_401(response)
    AssertionAdministratorsError.assert_authentication_error(response.json())

# TC-178: Admin > Administrators > Avatar Images – Validar error al eliminar imagen de avatar con token inválido
@allure.epic("Módulo de Administrador")
@allure.feature("Administrators > Avatar Images")
@allure.story("Eliminar imagen de avatar")
@allure.title("SYLIUS-178: Validar error al eliminar avatar con token inválido")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.administrator
@pytest.mark.avatar_images
@pytest.mark.security
@pytest.mark.functional_negative
@pytest.mark.high
def test_TC178_Error_eliminar_avatar_token_invalido(admin_id):
    url = AdministratorsEndpoint.avatar_delete(admin_id)
    headers = {"Authorization": "Bearer invalid_token"}
    response = SyliusRequest.delete(url, headers)
    AssertionStatusCode.assert_status_code_401(response)
    AssertionAdministratorsError.assert_authentication_error(response.json())

# TC-180: Admin > Administrators > Avatar Images – Verificar eliminación concurrente del mismo avatar
@allure.epic("Módulo de Administrador")
@allure.feature("Administrators > Avatar Images")
@allure.story("Eliminar imagen de avatar")
@allure.title("SYLIUS-180: Verificar eliminación concurrente del mismo avatar")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.administrator
@pytest.mark.avatar_images
@pytest.mark.functional_positive
@pytest.mark.functional_edgecase
@pytest.mark.concurrent
@pytest.mark.medium
def test_TC180_Eliminar_avatar_concurrente(auth_headers, admin_id, sample_avatar_file):
    url = AdministratorsEndpoint.avatar_upload(admin_id)
    delete_url = AdministratorsEndpoint.avatar_delete(admin_id)
    SyliusRequest.post(url, auth_headers, files=sample_avatar_file)
    response1 = SyliusRequest.delete(delete_url, auth_headers)
    response2 = SyliusRequest.delete(delete_url, auth_headers)
    AssertionStatusCode.assert_status_code_204(response1)
    AssertionStatusCode.assert_status_code_404(response2)

# TC-181: Admin > Administrators > Avatar Images – Validar error al eliminar imagen de avatar repetido
@allure.epic("Módulo de Administrador")
@allure.feature("Administrators > Avatar Images")
@allure.story("Eliminar imagen de avatar")
@allure.title("SYLIUS-181: Validar error al eliminar avatar repetido")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.administrator
@pytest.mark.avatar_images
@pytest.mark.functional_negative
@pytest.mark.functional_edgecase
@pytest.mark.medium
def test_TC181_Error_eliminar_avatar_repetido(auth_headers, admin_id, sample_avatar_file):
    url = AdministratorsEndpoint.avatar_upload(admin_id)
    delete_url = AdministratorsEndpoint.avatar_delete(admin_id)
    SyliusRequest.post(url, auth_headers, files=sample_avatar_file)
    SyliusRequest.delete(delete_url, auth_headers)
    response = SyliusRequest.delete(delete_url, auth_headers)
    AssertionStatusCode.assert_status_code_404(response)
    AssertionAdministratorsError.assert_avatar_not_found_error(response.json())

# TC-182: Admin > Administrators > Avatar Images – Verificar que un avatar eliminado no exista más
@allure.epic("Módulo de Administrador")
@allure.feature("Administrators > Avatar Images")
@allure.story("Eliminar imagen de avatar")
@allure.title("SYLIUS-182: Verificar que un avatar eliminado no exista más")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.administrator
@pytest.mark.avatar_images
@pytest.mark.functional_positive
@pytest.mark.high
def test_TC182_Verificar_avatar_eliminado_no_existe(auth_headers, admin_id, sample_avatar_file):
    url = AdministratorsEndpoint.avatar_upload(admin_id)
    delete_url = AdministratorsEndpoint.avatar_delete(admin_id)
    get_url = AdministratorsEndpoint.avatar_get(admin_id)
    SyliusRequest.post(url, auth_headers, files=sample_avatar_file)
    SyliusRequest.delete(delete_url, auth_headers)
    response = SyliusRequest.get(get_url, auth_headers)
    AssertionStatusCode.assert_status_code_404(response)
    AssertionAdministratorsError.assert_avatar_not_found_error(response.json())