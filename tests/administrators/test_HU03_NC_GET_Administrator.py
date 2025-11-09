import pytest
import allure
from src.services.request import SyliusRequest
from src.routes.administrators_endpoint import AdministratorsEndpoint
from src.assertions.status_code_assertion import AssertionStatusCode
from src.assertions.administrators.schema_assertion import AssertionAdministrators
from src.assertions.administrators.error_assertion import AssertionAdministratorsError
from src.assertions.administrators.view_content_assertion import AssertionAdministratorsContent

# SYLIUS-31: Admin > Administrators – Validar error al consultar un administrador sin token de autenticación
@allure.epic("Módulo de Administrador")
@allure.feature("Administrators")
@allure.story("Consultar administrador específico")
@allure.title("SYLIUS-31: Validar error al consultar un administrador sin token de autenticación")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.administrator
@pytest.mark.functional_negative
@pytest.mark.security
@pytest.mark.high
def test_TC31_Consultar_administrador_sin_token():
    headers = {}
    admin_id = 1
    url = f"{AdministratorsEndpoint.admins()}/{admin_id}"
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_401(response)
    AssertionAdministratorsError.assert_admin_error(response.json(), 401, "JWT Token not found")

# SYLIUS-32: Admin > Administrators – Validar error al consultar administrador con token inválido
@allure.epic("Módulo de Administrador")
@allure.feature("Administrators")
@allure.story("Consultar administrador específico")
@allure.title("SYLIUS-32: Validar error al consultar administrador con token inválido")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.administrator
@pytest.mark.functional_negative
@pytest.mark.security
@pytest.mark.high
def test_TC32_Consultar_administrador_token_invalido():
    headers = {"Authorization": "Bearer invalid_token"}
    admin_id = 1
    url = f"{AdministratorsEndpoint.admins()}/{admin_id}"
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_401(response)
    AssertionAdministratorsError.assert_admin_error(response.json(), 401, "Invalid JWT Token")

# SYLIUS-33: Admin > Administrators – Validar IDs únicos de administradores
@allure.epic("Módulo de Administrador")
@allure.feature("Administrators")
@allure.story("Consultar administrador específico")
@allure.title("SYLIUS-33: Validar IDs únicos de administradores")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.administrator
@pytest.mark.functional_positive
@pytest.mark.medium
def test_TC33_Validar_ids_unicos_administradores(view_admin):
    headers, _, _ = view_admin
    url = AdministratorsEndpoint.admins()
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_200(response)
    response_json = response.json()
    AssertionAdministrators.assert_list_schema(response_json)
    if isinstance(response_json, dict):
        admins = (
            response_json.get("hydra:member")
            or response_json.get("members")
            or [response_json]
        )
    elif isinstance(response_json, list):
        admins = response_json
    else:
        pytest.skip(f"Formato de respuesta inesperado: {type(response_json)}")
    ids = [admin.get("id") for admin in admins if "id" in admin]
    assert len(ids) == len(set(ids)), f"Los IDs de administradores no son únicos: {ids}"

# SYLIUS-34: Admin > Administrators – Verificar localización consistente
@allure.epic("Módulo de Administrador")
@allure.feature("Administrators")
@allure.story("Consultar administrador específico")
@allure.title("SYLIUS-34: Verificar localización consistente")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.administrator
@pytest.mark.functional_positive
@pytest.mark.medium
def test_TC34_Verificar_localizacion_consistente(view_admin):
    headers, _, _ = view_admin
    url = AdministratorsEndpoint.admins()
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_200(response)
    response_json = response.json()
    AssertionAdministrators.assert_list_schema(response_json)
    if isinstance(response_json, dict):
        admins = (
            response_json.get("hydra:member")
            or response_json.get("members")
            or [response_json]
        )
    elif isinstance(response_json, list):
        admins = response_json
    else:
        pytest.skip(f"Formato de respuesta inesperado: {type(response_json)}")
    locales = [admin.get("localeCode") for admin in admins if "localeCode" in admin]
    if not locales:
        pytest.skip("No hay datos de localización (localeCode) en la respuesta.")
    assert all(locale is not None for locale in locales), (
        f"Hay administradores sin localeCode definido: {locales}"
    )

# SYLIUS-35: Admin > Administrators – Obtener administrador activo
@allure.epic("Módulo de Administrador")
@allure.feature("Administrators")
@allure.story("Consultar administrador específico")
@allure.title("SYLIUS-35: Obtener administradores activos")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.administrator
@pytest.mark.functional_positive
@pytest.mark.medium
def test_TC35_Obtener_administrador_activo(view_admin):
    headers, _, _ = view_admin
    url = AdministratorsEndpoint.admins_with_params(enabled=True)
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_200(response)
    response_json = response.json()
    AssertionAdministrators.assert_list_schema(response_json)
    AssertionAdministratorsContent.assert_admin_collection(response_json, params={"enabled": True})

# SYLIUS-36: Admin > Administrators – Obtener administrador inactivo
@allure.epic("Módulo de Administrador")
@allure.feature("Administrators")
@allure.story("Consultar administrador específico")
@allure.title("SYLIUS-36: Obtener administradores inactivos")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.administrator
@pytest.mark.functional_positive
@pytest.mark.medium
def test_TC36_Obtener_administrador_inactivo(view_admin):
    headers, _, _ = view_admin
    url = AdministratorsEndpoint.admins_with_params(enabled=False)
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_200(response)
    response_json = response.json()
    AssertionAdministrators.assert_list_schema(response_json)
    AssertionAdministratorsContent.assert_admin_collection(response_json, params={"enabled": False})

# SYLIUS-37: Admin > Administrators - Ingresar ID igual a 12345
# SYLIUS-38: Admin > Administrators - Validar error al ingresar ID igual a 0
# SYLIUS-39: Admin > Administrators - Validar error al ingresar ID string igual a "uno"
# SYLIUS-40: Admin > Administrators - Validar error al ingresar ID negativo igual a -1
# SYLIUS-41: Admin > Administrators - Validar error al ingresar ID decimal igual a 1.5
@allure.epic("Módulo de Administrador")
@allure.feature("Administrators")
@allure.story("Consultar administrador específico")
@allure.title("SYLIUS-37 - SYLIUS-41: Validar error al ingresar IDs no válidos")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.administrator
@pytest.mark.functional_negative
@pytest.mark.medium
@pytest.mark.parametrize("admin_id, expected_status", [
    (12345, 404),
    (0, 404),
    ("uno", 404),
    (-1, 404),
    (1.5, 404)
])
def test_TC_Admin_Administrators_validar_parametros_ID(auth_headers, admin_id, expected_status):
    headers = auth_headers
    url = f"{AdministratorsEndpoint.admins()}/{admin_id}"
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code(response, expected_status)