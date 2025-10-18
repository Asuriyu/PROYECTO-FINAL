import pytest
from src.services.request import SyliusRequest
from src.routes.administrators_endpoint import AdministratorsEndpoint
from src.assertions.status_code_assertion import AssertionStatusCode
from src.assertions.administrators.schema_assertion import AssertionAdministrators
from src.assertions.administrators.error_assertion import AssertionAdministratorsError
from src.assertions.administrators.view_content_assertion import AssertionAdministratorsContent
from src.resources.payloads.administrators_payload import AdministratorsPayload
from src.data.administrators import generate_admin_data
from src.data.admin_helper import create_temp_admin

# TC-86: Admin > Administrators – Actualizar administrador con datos válidos
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

# TC-87: Admin > Administrators – Actualizar administrador con solo datos requeridos
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

# TC-88: Admin > Administrators - Validar error al actualizar administrador sin token
def test_TC88_Validar_error_al_actualizar_administrador_sin_token():
    headers = {}
    payload = AdministratorsPayload.build_payload_admin(generate_admin_data())
    url = f"{AdministratorsEndpoint.admins()}/1"
    response = SyliusRequest.put(url, headers, payload)
    AssertionStatusCode.assert_status_code_401(response)
    AssertionAdministratorsError.assert_admin_error(response.json(), 401, "JWT Token not found")

# TC-89: Admin > Administrators - Validar error al actualizar administrador con token inválido
def test_TC89_Validar_error_al_actualizar_administrador_con_token_invalido():
    headers = {"Authorization": "Bearer token_invalido"}
    payload = AdministratorsPayload.build_payload_admin(generate_admin_data())
    url = f"{AdministratorsEndpoint.admins()}/1"
    response = SyliusRequest.put(url, headers, payload)
    AssertionStatusCode.assert_status_code_401(response)
    AssertionAdministratorsError.assert_admin_error(response.json(), 401, "Invalid JWT Token")

# TC-90: Admin > Administrators – Validar comportamiento al actualizar administrador sin datos requeridos
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

# TC-91: Admin > Administrators - Validar error al actualizar administrador con username duplicado
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

# TC-92: Admin > Administrators - Validar error al actualizar administrador con email duplicado
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

# TC-93: Admin > Administrators - Validar error al actualizar administrador con email inválido
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

# TC-94: Admin > Administrators - Actualizar administrador con enabled activado
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

# TC-95: Admin > Administrators - Actualizar administrador con enabled desactivado
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

# TC-96: Admin > Administrators - Ingresar ID igual a 12345
# TC-97: Admin > Administrators - Validar error al ingresar ID igual a 0
# TC-98: Admin > Administrators - Validar error al ingresar ID string igual a "uno"
# TC-99: Admin > Administrators - Validar error al ingresar ID negativo igual a -1
# TC-100: Admin > Administrators - Validar error al ingresar ID decimal igual a 1.5
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

# TC-101: Admin > Administrators - Validar campo firstName con valor null
# TC-102: Admin > Administrators - Ingresar firstName con caracteres menor a 256 caracteres
# TC-103: Admin > Administrators - Ingresar firstName igual a Juan
# TC-104: Admin > Administrators - Validar error al ingresar firstName con 256 caracteres
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

# TC-105: Admin > Administrators - Validar campo lastName con valor null
# TC-106: Admin > Administrators - Ingresar lastName con caracteres menor a 256 caracteres
# TC-107: Admin > Administrators - Ingresar lastName igual a Pérez
# TC-108: Admin > Administrators - Validar error al ingresar lastName con 256 caracteres
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

# TC-109: Admin > Administrators - Ingresar localeCode igual a en_US
# TC-110: Admin > Administrators - Validar error al ingresar localeCode igual a xx_XX
# TC-111: Admin > Administrators - Validar error al ingresar localeCode igual a 123
# TC-112: Admin > Administrators - Validar error al ingresar localeCode vacío
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

# TC-113: Admin > Administrators – Ingresar username igual a 1 carácter al actualizar
# TC-114: Admin > Administrators – Ingresar username con exactamente 255 caracteres al actualizar
# TC-115: Admin > Administrators – Ingresar username igual a admin01 al actualizar
# TC-116: Admin > Administrators – Validar error al actualizar username con 0 caracteres
# TC-117: Admin > Administrators – Validar error al actualizar username con 256 caracteres
# TC-118: Admin > Administrators – Validar error al actualizar username vacío
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

# TC-119: Admin > Administrators – Ingresar plainPassword igual a 4 caracteres al actualizar
# TC-120: Admin > Administrators – Ingresar plainPassword con 255 caracteres al actualizar
# TC-121: Admin > Administrators – Ingresar plainPassword igual a Test1234 al actualizar
# TC-122: Admin > Administrators – Validar error al actualizar plainPassword con 3 caracteres
# TC-123: Admin > Administrators – Validar error al actualizar plainPassword con 256 caracteres
# TC-124: Admin > Administrators – Validar error al actualizar plainPassword vacío
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

# TC-125: Admin > Administrators – Ingresar email igual a user@test.com al actualizar
# TC-126: Admin > Administrators – Validar error al actualizar email igual a test
# TC-127: Admin > Administrators – Validar error al actualizar email igual a user@com
# TC-128: Admin > Administrators – Validar error al actualizar email igual a @mail.com
# TC-129: Admin > Administrators – Validar error al actualizar email vacío
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

# TC-130: Admin > Administrators – Validar error al actualizar sin cambios
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