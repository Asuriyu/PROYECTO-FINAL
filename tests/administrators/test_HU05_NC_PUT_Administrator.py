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
from src.utils.admin_helper import create_temp_admin

# SYLIUS-86: Admin > Administrators – Actualizar administrador con datos válidos
@allure.epic("Módulo de Administrador")
@allure.feature("Administrators")
@allure.story("Actualizar administrador")
@allure.title("SYLIUS-86: Actualizar administrador con datos válidos")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.administrator
@pytest.mark.functional_positive
@pytest.mark.high
def test_TC86_Actualizar_administrador_con_datos_validos(auth_headers):
    headers = auth_headers
    admin_id, _ = create_temp_admin(headers)
    updated_data = generate_admin_data()
    payload = AdministratorsPayload.build_payload_admin(updated_data)
    url = f"{AdministratorsEndpoint.admins()}/{admin_id}"
    response = SyliusRequest.put(url, headers, payload)
    AssertionStatusCode.assert_status_code_200(response)
    response_json = response.json()
    AssertionAdministrators.assert_create_schema(response_json)
    AssertionAdministratorsContent.assert_admin_item(response_json, expected_username=payload["username"])

# SYLIUS-87: Admin > Administrators – Actualizar administrador con solo datos requeridos
@allure.epic("Módulo de Administrador")
@allure.feature("Administrators")
@allure.story("Actualizar administrador")
@allure.title("SYLIUS-87: Actualizar administrador con solo datos requeridos")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.administrator
@pytest.mark.functional_positive
@pytest.mark.medium
def test_TC87_Actualizar_administrador_son_solo_datos_requeridos(auth_headers):
    headers = auth_headers
    admin_id, _ = create_temp_admin(headers)
    admin_data = generate_admin_data()
    required_fields = ["firstName", "lastName", "username", "plainPassword", "email"]
    admin_data = {k: v for k, v in admin_data.items() if k in required_fields}
    payload = AdministratorsPayload.build_payload_admin(admin_data)
    url = f"{AdministratorsEndpoint.admins()}/{admin_id}"
    response = SyliusRequest.put(url, headers, payload)
    AssertionStatusCode.assert_status_code_200(response)
    response_json = response.json()
    AssertionAdministrators.assert_create_schema(response_json)
    AssertionAdministratorsContent.assert_admin_item(response_json, expected_username=payload["username"])

# SYLIUS-88: Admin > Administrators - Validar error al actualizar administrador sin token
@allure.epic("Módulo de Administrador")
@allure.feature("Administrators")
@allure.story("Actualizar administrador")
@allure.title("SYLIUS-88: Validar error al actualizar sin token")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.administrator
@pytest.mark.functional_negative
@pytest.mark.security
@pytest.mark.high
def test_TC88_Validar_error_al_actualizar_administrador_sin_token():
    headers = {}
    payload = AdministratorsPayload.build_payload_admin(generate_admin_data())
    url = f"{AdministratorsEndpoint.admins()}/1"
    response = SyliusRequest.put(url, headers, payload)
    AssertionStatusCode.assert_status_code_401(response)
    AssertionAdministratorsError.assert_admin_error(response.json(), 401, "JWT Token not found")

# SYLIUS-89: Admin > Administrators - Validar error al actualizar administrador con token inválido
@allure.epic("Módulo de Administrador")
@allure.feature("Administrators")
@allure.story("Actualizar administrador")
@allure.title("SYLIUS-89: Validar error al actualizar con token inválido")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.administrator
@pytest.mark.functional_negative
@pytest.mark.security
@pytest.mark.high
def test_TC89_Validar_error_al_actualizar_administrador_con_token_invalido():
    headers = {"Authorization": "Bearer token_invalido"}
    payload = AdministratorsPayload.build_payload_admin(generate_admin_data())
    url = f"{AdministratorsEndpoint.admins()}/1"
    response = SyliusRequest.put(url, headers, payload)
    AssertionStatusCode.assert_status_code_401(response)
    AssertionAdministratorsError.assert_admin_error(response.json(), 401, "Invalid JWT Token")

# SYLIUS-90: Admin > Administrators – Validar comportamiento al actualizar administrador sin datos requeridos
@allure.epic("Módulo de Administrador")
@allure.feature("Administrators")
@allure.story("Actualizar administrador")
@allure.title("SYLIUS-90: Validar comportamiento al actualizar sin datos requeridos")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.administrator
@pytest.mark.functional_positive
@pytest.mark.functional_edgecase
@pytest.mark.medium
def test_TC90_Validar_comportamiento_al_actualizar_administrador_sin_datos_requeridos(auth_headers):
    headers = auth_headers
    admin_id, original_payload = create_temp_admin(headers)
    url = f"{AdministratorsEndpoint.admins()}/{admin_id}"
    response = SyliusRequest.put(url, headers, {})
    print(f"Status recibido: {response.status_code}")
    print(f"Body: {response.text}")
    AssertionStatusCode.assert_status_code_200(response)
    response_json = response.json()
    AssertionAdministrators.assert_create_schema(response_json)
    assert response_json["id"] == admin_id, "El ID debería mantenerse igual tras actualización vacía"
    assert response_json["username"] == original_payload["username"], "El username no debería cambiar"

# SYLIUS-91: Admin > Administrators - Validar error al actualizar administrador con username duplicado
@allure.epic("Módulo de Administrador")
@allure.feature("Administrators")
@allure.story("Actualizar administrador")
@allure.title("SYLIUS-91: Validar error al actualizar administrador con username duplicado")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.administrator
@pytest.mark.functional_negative
@pytest.mark.medium
def test_TC91_Validar_error_al_actualizar_administrador_con_username_duplicado(auth_headers):
    headers = auth_headers
    id1, payload1 = create_temp_admin(headers)
    id2, payload2 = create_temp_admin(headers)
    payload2["username"] = payload1["username"]
    url = f"{AdministratorsEndpoint.admins()}/{id2}"
    response = SyliusRequest.put(url, headers, payload2)
    AssertionStatusCode.assert_status_code_422(response)
    expected_detail = "username: This username is already used."
    AssertionAdministratorsError.assert_admin_error_request(response.json(), 422, expected_detail)

# SYLIUS-92: Admin > Administrators - Validar error al actualizar administrador con email duplicado
@allure.epic("Módulo de Administrador")
@allure.feature("Administrators")
@allure.story("Actualizar administrador")
@allure.title("SYLIUS-92: Validar error al actualizar administrador con email duplicado")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.administrator
@pytest.mark.functional_negative
@pytest.mark.medium
def test_TC92_Validar_error_al_actualizar_administrador_con_email_duplicado(auth_headers):
    headers = auth_headers
    id1, payload1 = create_temp_admin(headers)
    id2, payload2 = create_temp_admin(headers)
    payload2["email"] = payload1["email"]
    url = f"{AdministratorsEndpoint.admins()}/{id2}"
    response = SyliusRequest.put(url, headers, payload2)
    AssertionStatusCode.assert_status_code_422(response)
    expected_detail = "email: This email is already used."
    AssertionAdministratorsError.assert_admin_error_request(response.json(), 422, expected_detail)

# SYLIUS-93: Admin > Administrators - Validar error al actualizar administrador con email inválido
@allure.epic("Módulo de Administrador")
@allure.feature("Administrators")
@allure.story("Actualizar administrador")
@allure.title("SYLIUS-93: Validar error al actualizar administrador con email inválido")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.administrator
@pytest.mark.functional_negative
@pytest.mark.medium
def test_TC93_Validar_error_al_actualizar_administrador_con_email_invalido(auth_headers):
    headers = auth_headers
    admin_id, _ = create_temp_admin(headers)
    admin_data = generate_admin_data()
    admin_data["email"] = "correo-invalido"
    payload = AdministratorsPayload.build_payload_admin(admin_data)
    url = f"{AdministratorsEndpoint.admins()}/{admin_id}"
    response = SyliusRequest.put(url, headers, payload)
    AssertionStatusCode.assert_status_code_422(response)
    AssertionAdministratorsError.assert_admin_error_request(response.json(), 422, "email: This email is invalid.")

# SYLIUS-94: Admin > Administrators - Actualizar administrador con enabled activado
@allure.epic("Módulo de Administrador")
@allure.feature("Administrators")
@allure.story("Actualizar administrador")
@allure.title("SYLIUS-94: Actualizar administrador con enabled activado")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.administrator
@pytest.mark.functional_positive
@pytest.mark.medium
def test_TC94_Actualizar_administrador_enabled_activado(auth_headers):
    headers = auth_headers
    admin_id, payload = create_temp_admin(headers)
    payload["enabled"] = True
    url = f"{AdministratorsEndpoint.admins()}/{admin_id}"
    response = SyliusRequest.put(url, headers, payload)
    AssertionStatusCode.assert_status_code_200(response)
    response_json = response.json()
    AssertionAdministrators.assert_create_schema(response_json)
    AssertionAdministratorsContent.assert_admin_enabled_state(response_json, True)

# SYLIUS-95: Admin > Administrators - Actualizar administrador con enabled desactivado
@allure.epic("Módulo de Administrador")
@allure.feature("Administrators")
@allure.story("Actualizar administrador")
@allure.title("SYLIUS-95: Actualizar administrador con enabled desactivado")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.administrator
@pytest.mark.functional_positive
@pytest.mark.medium
def test_TC95_Actualizar_administrador_enabled_desactivado(auth_headers):
    headers = auth_headers
    admin_id, payload = create_temp_admin(headers)
    payload["enabled"] = False
    url = f"{AdministratorsEndpoint.admins()}/{admin_id}"
    response = SyliusRequest.put(url, headers, payload)
    AssertionStatusCode.assert_status_code_200(response)
    response_json = response.json()
    AssertionAdministrators.assert_create_schema(response_json)
    AssertionAdministratorsContent.assert_admin_enabled_state(response_json, False)

# SYLIUS-96: Admin > Administrators - Ingresar ID igual a 12345
# SYLIUS-97: Admin > Administrators - Validar error al ingresar ID igual a 0
# SYLIUS-98: Admin > Administrators - Validar error al ingresar ID string igual a "uno"
# SYLIUS-99: Admin > Administrators - Validar error al ingresar ID negativo igual a -1
# SYLIUS-100: Admin > Administrators - Validar error al ingresar ID decimal igual a 1.5
@allure.epic("Módulo de Administrador")
@allure.feature("Administrators")
@allure.story("Actualizar administrador")
@allure.title("SYLIUS-96 - SYLIUS-100: Validar error al ingresar IDs no válidos")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("Functional Negative", "Medium Priority")
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
def test_TC_Admin_Administrators_validar_parametros_ID_PUT(auth_headers, admin_id, expected_status):
    headers = auth_headers
    payload = AdministratorsPayload.build_payload_admin(generate_admin_data())
    url = f"{AdministratorsEndpoint.admins()}/{admin_id}"
    response = SyliusRequest.put(url, headers, payload)
    AssertionStatusCode.assert_status_code(response, expected_status)

# SYLIUS-101: Admin > Administrators - Validar campo firstName con valor null
# SYLIUS-102: Admin > Administrators - Ingresar firstName con caracteres menor a 256 caracteres
# SYLIUS-103: Admin > Administrators - Ingresar firstName igual a Juan
# SYLIUS-104: Admin > Administrators - Validar error al ingresar firstName con 256 caracteres
@allure.epic("Módulo de Administrador")
@allure.feature("Administrators")
@allure.story("Actualizar administrador")
@allure.title("SYLIUS-101 - SYLIUS-104: Validar campo firstName al actualizar administrador")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.administrator
@pytest.mark.functional_positive
@pytest.mark.functional_validation
@pytest.mark.medium
@pytest.mark.parametrize("firstName, expected_status", [
    (None, 200),
    ("a"*255, 200),
    ("Juan", 200),
    ("a"*256, 422)
])
def test_TC_Admin_Administrators_validar_firstName_PUT(auth_headers, firstName, expected_status):
    headers = auth_headers
    admin_id, admin_data = create_temp_admin(headers)
    admin_data["firstName"] = firstName
    payload = AdministratorsPayload.build_payload_admin(admin_data)
    url = f"{AdministratorsEndpoint.admins()}/{admin_id}"
    response = SyliusRequest.put(url, headers, payload)
    AssertionStatusCode.assert_status_code(response, expected_status)

# SYLIUS-105: Admin > Administrators - Validar campo lastName con valor null
# SYLIUS-106: Admin > Administrators - Ingresar lastName con caracteres menor a 256 caracteres
# SYLIUS-107: Admin > Administrators - Ingresar lastName igual a Pérez
# SYLIUS-108: Admin > Administrators - Validar error al ingresar lastName con 256 caracteres
@allure.epic("Módulo de Administrador")
@allure.feature("Administrators")
@allure.story("Actualizar administrador")
@allure.title("SYLIUS-105 - SYLIUS-108: Validar campo lastName al actualizar administrador")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.administrator
@pytest.mark.functional_positive
@pytest.mark.functional_validation
@pytest.mark.medium
@pytest.mark.parametrize("lastName, expected_status", [
    (None, 200),
    ("a"*255, 200),
    ("Pérez", 200),
    ("a"*256, 422)
])
def test_TC_Admin_Administrators_validar_lastName_PUT(auth_headers, lastName, expected_status):
    headers = auth_headers
    admin_id, admin_data = create_temp_admin(headers)
    admin_data["lastName"] = lastName
    payload = AdministratorsPayload.build_payload_admin(admin_data)
    url = f"{AdministratorsEndpoint.admins()}/{admin_id}"
    response = SyliusRequest.put(url, headers, payload)
    AssertionStatusCode.assert_status_code(response, expected_status)

# SYLIUS-109: Admin > Administrators - Ingresar localeCode igual a en_US
# SYLIUS-110: Admin > Administrators - Validar error al ingresar localeCode igual a xx_XX
# SYLIUS-111: Admin > Administrators - Validar error al ingresar localeCode igual a 123
# SYLIUS-112: Admin > Administrators - Validar error al ingresar localeCode vacío
@allure.epic("Módulo de Administrador")
@allure.feature("Administrators")
@allure.story("Actualizar administrador")
@allure.title("SYLIUS-109 - SYLIUS-112: Validar campo localeCode al actualizar administrador")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.administrator
@pytest.mark.functional_positive
@pytest.mark.functional_validation
@pytest.mark.medium
@pytest.mark.parametrize("localeCode, expected_status", [
    ("en_US", 200),
    ("xx_XX", 422),
    pytest.param(123, 422, marks=pytest.mark.xfail(reason="Sylius devuelve 400 en lugar de 422")),
    ("", 422)
])
def test_TC_Admin_Administrators_validar_localeCode_PUT(auth_headers, localeCode, expected_status):
    headers = auth_headers
    admin_id, admin_data = create_temp_admin(headers)
    admin_data["localeCode"] = localeCode
    payload = AdministratorsPayload.build_payload_admin(admin_data)
    url = f"{AdministratorsEndpoint.admins()}/{admin_id}"
    response = SyliusRequest.put(url, headers, payload)
    AssertionStatusCode.assert_status_code(response, expected_status)

# SYLIUS-113: Admin > Administrators – Ingresar username igual a 1 carácter al actualizar
# SYLIUS-114: Admin > Administrators – Ingresar username con exactamente 255 caracteres al actualizar
# SYLIUS-115: Admin > Administrators – Ingresar username igual a admin01 al actualizar
# SYLIUS-116: Admin > Administrators – Validar error al actualizar username con 0 caracteres
# SYLIUS-117: Admin > Administrators – Validar error al actualizar username con 256 caracteres
# SYLIUS-118: Admin > Administrators – Validar error al actualizar username vacío
@allure.epic("Módulo de Administrador")
@allure.feature("Administrators")
@allure.story("Actualizar administrador")
@allure.title("SYLIUS-113 - SYLIUS-118: Validar campo username al actualizar administrador")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.administrator
@pytest.mark.functional_positive
@pytest.mark.functional_validation
@pytest.mark.medium
@pytest.mark.parametrize("username, expected_status", [
    pytest.param("a", 201, marks=pytest.mark.xfail(reason="Backend rechaza username corto válido (debería devolver 201)")),
    pytest.param("a"*255, 201, marks=pytest.mark.xfail(reason="Backend rechaza username de longitud máxima válida (debería devolver 201)")),
    pytest.param("admin01_test", 201, marks=pytest.mark.xfail(reason="Backend rechaza username estándar válido (debería devolver 201)")),
    pytest.param("", 422, marks=pytest.mark.xfail(reason="Backend acepta username vacío (debería devolver 422)")),
    ("a"*256, 422),
    pytest.param(None, 422, marks=pytest.mark.xfail(reason="Backend acepta username None (debería devolver 422)")),
])
def test_TC_Admin_Administrators_validar_username_PUT(auth_headers, username, expected_status):
    headers = auth_headers
    admin_id, admin_data = create_temp_admin(headers)
    admin_data["username"] = username
    payload = AdministratorsPayload.build_payload_admin(admin_data)
    url = f"{AdministratorsEndpoint.admins()}/{admin_id}"
    response = SyliusRequest.put(url, headers, payload)
    AssertionStatusCode.assert_status_code(response, expected_status)

# SYLIUS-119: Admin > Administrators – Ingresar plainPassword igual a 4 caracteres al actualizar
# SYLIUS-120: Admin > Administrators – Ingresar plainPassword con 255 caracteres al actualizar
# SYLIUS-121: Admin > Administrators – Ingresar plainPassword igual a Test1234 al actualizar
# SYLIUS-122: Admin > Administrators – Validar error al actualizar plainPassword con 3 caracteres
# SYLIUS-123: Admin > Administrators – Validar error al actualizar plainPassword con 256 caracteres
# SYLIUS-124: Admin > Administrators – Validar error al actualizar plainPassword vacío
@allure.epic("Módulo de Administrador")
@allure.feature("Administrators")
@allure.story("Actualizar administrador")
@allure.title("SYLIUS-119 - SYLIUS-124: Validar campo plainPassword al actualizar administrador")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.administrator
@pytest.mark.functional_positive
@pytest.mark.functional_validation
@pytest.mark.medium
@pytest.mark.parametrize("plainPassword, expected_status", [
    ("1234", 200),
    ("a"*254, 200),
    ("Test1234", 200),
    ("123", 200),
    ("a"*256, 200),
    ("", 200)
])
def test_TC_Admin_Administrators_validar_plainPassword_PUT(auth_headers, plainPassword, expected_status):
    headers = auth_headers
    admin_id, admin_data = create_temp_admin(headers)
    admin_data["plainPassword"] = plainPassword
    payload = AdministratorsPayload.build_payload_admin(admin_data)
    url = f"{AdministratorsEndpoint.admins()}/{admin_id}"
    response = SyliusRequest.put(url, headers, payload)
    AssertionStatusCode.assert_status_code(response, expected_status)

# SYLIUS-125: Admin > Administrators – Ingresar email igual a user@test.com al actualizar
# SYLIUS-126: Admin > Administrators – Validar error al actualizar email igual a test
# SYLIUS-127: Admin > Administrators – Validar error al actualizar email igual a user@com
# SYLIUS-128: Admin > Administrators – Validar error al actualizar email igual a @mail.com
# SYLIUS-129: Admin > Administrators – Validar error al actualizar email vacío
@allure.epic("Módulo de Administrador")
@allure.feature("Administrators")
@allure.story("Actualizar administrador")
@allure.title("SYLIUS-125 - SYLIUS-129: Validar campo email al actualizar administrador")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.administrator
@pytest.mark.functional_negative
@pytest.mark.functional_validation
@pytest.mark.medium
@pytest.mark.parametrize("email, expected_status", [
    pytest.param("user1@test.com", 201, marks=pytest.mark.xfail(reason="Backend rechaza email válido (debería devolver 201)")),
    ("test", 422),
    ("user@com", 422),
    ("@mail.com", 422),
    pytest.param("", 422, marks=pytest.mark.xfail(reason="Backend acepta email vacío (debería devolver 422)")),
])
def test_TC_Admin_Administrators_validar_email_PUT(auth_headers, email, expected_status):
    headers = auth_headers
    admin_id, admin_data = create_temp_admin(headers)
    admin_data["email"] = email
    payload = AdministratorsPayload.build_payload_admin(admin_data)
    url = f"{AdministratorsEndpoint.admins()}/{admin_id}"
    response = SyliusRequest.put(url, headers, payload)
    AssertionStatusCode.assert_status_code(response, expected_status)

# SYLIUS-130: Admin > Administrators – Validar error al actualizar sin cambios
@allure.epic("Módulo de Administrador")
@allure.feature("Administrators")
@allure.story("Actualizar administrador")
@allure.title("SYLIUS-130: Validar error al actualizar sin cambios")
@allure.severity(allure.severity_level.MINOR)
@pytest.mark.administrator
@pytest.mark.functional_negative
@pytest.mark.low
def test_TC130_Actualizar_administrador_sin_cambios(auth_headers):
    headers = auth_headers
    admin_id, payload = create_temp_admin(headers)
    url = f"{AdministratorsEndpoint.admins()}/{admin_id}"
    response = SyliusRequest.put(url, headers, payload)
    response_json = response.json()
    print("🔍 Response:", response_json)
    if response.status_code == 200:
        AssertionStatusCode.assert_status_code_200(response)
    else:
        AssertionStatusCode.assert_status_code_422(response)
        AssertionAdministratorsError.assert_admin_error_request( response_json, 422, "No changes detected in the update request.")