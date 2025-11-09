import pytest
import allure
from src.services.request import SyliusRequest
from src.routes.administrators_endpoint import AdministratorsEndpoint
from src.assertions.status_code_assertion import AssertionStatusCode
from src.assertions.administrators.schema_assertion import AssertionAdministrators
from src.assertions.administrators.error_assertion import AssertionAdministratorsError
from src.assertions.administrators.view_content_assertion import AssertionAdministratorsContent
from src.resources.payloads.administrators_payload import AdministratorsPayload
from src.data.administrators import generate_admin_data

# SYLIUS-16: Admin > Administrators – Obtener lista completa de administradores
@allure.epic("Modulo de Administrador")
@allure.feature("Administrators")
@allure.story("Listar administradores")
@allure.title("SYLIUS-16: Obtener lista completa de administradores")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.administrator
@pytest.mark.functional_positive
@pytest.mark.high
def test_TC16_Obtener_lista_de_administradores(view_admin):
    headers, _, _ = view_admin
    url = AdministratorsEndpoint.admins()
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_200(response)
    response_json = response.json()
    AssertionAdministrators.assert_list_schema(response_json)
    AssertionAdministratorsContent.assert_admin_collection(response_json)

# SYLIUS-17: Admin > Administrators – Validar error al listar administradores sin token de autenticación   
@allure.epic("Modulo de Administrador")
@allure.feature("Administrators")
@allure.story("Listar administradores")
@allure.title("SYLIUS-17: Validar error al listar administradores sin token de autenticación")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.administrator
@pytest.mark.functional_negative
@pytest.mark.high
@pytest.mark.security
def test_TC17_Listar_administradores_sin_token():
    headers = {}
    url = AdministratorsEndpoint.admins()
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_401(response)
    AssertionAdministratorsError.assert_admin_error(response.json(), 401, "JWT Token not found")

# SYLIUS-18: Admin > Administrators – Validar error al listar administradores con token inválido
@allure.epic("Modulo de Administrador")
@allure.feature("Administrators")
@allure.story("Listar administradores")
@allure.title("SYLIUS-18: Validar error al listar administradores con token inválido")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.administrator
@pytest.mark.functional_negative
@pytest.mark.high
@pytest.mark.security
def test_TC18_Listar_administradores_con_token_invalido():
    headers = {"Authorization": "Bearer invalid_token"}
    url = AdministratorsEndpoint.admins()
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_401(response)
    AssertionAdministratorsError.assert_admin_error(response.json(), 401, "Invalid JWT Token")

# SYLIUS-19: Admin > Administrators – Obtener lista de administrador con página igual a 1   
# SYLIUS-20: Admin > Administrators – Obtener lista de administrador con página mínima válida y cantidad igual 1   
# SYLIUS-21: Admin > Administrators – Obtener lista de administrador con página mínima válida y cantidad igual a 0 
@allure.epic("Modulo de Administrador")
@allure.feature("Administrators")
@allure.story("SYLIUS-19 - SYLIUS-21: Listar administradores con paginación válida")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.administrator
@pytest.mark.functional_positive
@pytest.mark.medium
@pytest.mark.parametrize("page, itemsPerPage", [
    (1, None),
    (1, 1),
    (1, 0)
])
def test_TC_Obtener_lista_de_administradores_con_paginacion_valida(view_admin, page, itemsPerPage):
    headers, _, _ = view_admin
    params = {"page": page, "itemsPerPage": itemsPerPage}
    params = {k: v for k, v in params.items() if v is not None}
    url = AdministratorsEndpoint.admins_with_params(**params)
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_200(response)
    AssertionAdministratorsContent.assert_admin_collection(response.json(), params=params)

# SYLIUS-22: Admin > Administrators – Validar error al usar página igual a 0 y cantidad válida   
# SYLIUS-23: Admin > Administrators – Validar error al usar página negativa igual a -1 y cantidad válida   
# SYLIUS-24: Admin > Administrators – Validar error al usar página decimal igual a 1.5 y cantidad válida   
# SYLIUS-25: Admin > Administrators – Validar error al usar página string igual a “uno” y cantidad válida   
# SYLIUS-26: Admin > Administrators – Validar error al usar página vacía y cantidad válida   
# SYLIUS-27: Admin > Administrators – Validar error al usar página mínima válida y cantidad negativa igual a -1   
# SYLIUS-28: Admin > Administrators – Validar error al usar página mínima válida y cantidad decimal igual a 1.5   
# SYLIUS-29: Admin > Administrators – Validar error al usar página mínima válida y cantidad string igual a “uno”   
# SYLIUS-30: Admin > Administrators – Validar error al usar página mínima válida y cantidad vacía
@allure.epic("Modulo de Administrador")
@allure.feature("Administrators")
@allure.story("SYLIUS-22 - SYLIUS-30: Listar administradores con paginación inválida")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.administrator
@pytest.mark.functional_negative
@pytest.mark.medium
@pytest.mark.parametrize("page, itemsPerPage", [
    (0, 1),
    (-1, 1),
    pytest.param(1.5, 1, marks=pytest.mark.xfail(reason="BUGXX: page decimal rompe la URL")),
    ("uno", 1),
    (" ", 1),
    (1, -1),
    pytest.param(1, 1.5, marks=pytest.mark.xfail(reason="BUGXX: itemsPerPage decimal rompe la URL")),
    pytest.param(1, "uno", marks=pytest.mark.xfail(reason="BUGXX: itemsPerPage string rompe la URL")),
    pytest.param(1, None, marks=pytest.mark.xfail(reason="BUGXX: itemsPerPage vacío rompe la URL"))
])
def test_TC_Obtener_lista_de_administradores_con_paginacion_invalida(view_admin, page, itemsPerPage):
    headers, _, _ = view_admin
    params = {"page": page, "itemsPerPage": itemsPerPage}
    params = {k: v for k, v in params.items() if v is not None}
    url = AdministratorsEndpoint.admins_with_params(**params)
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_400(response)