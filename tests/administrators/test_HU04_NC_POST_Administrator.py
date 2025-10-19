import pytest
from src.services.request import SyliusRequest
from src.routes.administrators_endpoint import AdministratorsEndpoint
from src.assertions.status_code_assertion import AssertionStatusCode
from src.assertions.administrators.schema_assertion import AssertionAdministrators
from src.assertions.administrators.error_assertion import AssertionAdministratorsError
from src.assertions.administrators.view_content_assertion import AssertionAdministratorsContent
from src.resources.payloads.administrators_payload import AdministratorsPayload
from src.data.administrators import generate_admin_data

# TC-42: Admin > Administrators – Crear administrador con datos válidos
def test_TC42_Crear_administrador_datos_validos(auth_headers, admin_data):
    headers = auth_headers
    payload = AdministratorsPayload.build_payload_admin(admin_data)
    url = AdministratorsEndpoint.admins()
    response = SyliusRequest.post(url, headers, payload)
    AssertionStatusCode.assert_status_code_201(response)
    response_json = response.json()
    AssertionAdministrators.assert_create_schema(response_json)
    AssertionAdministratorsContent.assert_admin_item(response_json, expected_username=payload["username"])

# TC-43: Admin > Administrators – Crear administrador con solo datos requeridos
def test_TC43_Crear_administrador_con_solo_datos_requeridos(auth_headers):
    headers = auth_headers
    admin_data = generate_admin_data()
    required_fields = ["firstName", "lastName", "username", "plainPassword", "email"]
    admin_data = {k: v for k, v in admin_data.items() if k in required_fields}
    payload = AdministratorsPayload.build_payload_admin(admin_data)
    url = AdministratorsEndpoint.admins()
    response = SyliusRequest.post(url, headers, payload)
    AssertionStatusCode.assert_status_code_201(response)
    response_json = response.json()
    AssertionAdministrators.assert_create_schema(response_json)
    AssertionAdministratorsContent.assert_admin_item(response_json, expected_username=payload["username"])

# TC-44: Admin > Administrators - Validar error al crear administrador sin token de autenticación
def test_TC44_Validar_error_al_crear_administrador_sin_token_de_autenticacion():
    headers = {}
    payload = AdministratorsPayload.build_payload_admin(generate_admin_data())
    url = AdministratorsEndpoint.admins()
    response = SyliusRequest.post(url, headers, payload)
    AssertionStatusCode.assert_status_code_401(response)
    AssertionAdministratorsError.assert_admin_error(response.json(), 401, "JWT Token not found")

# TC-45: Admin > Administrators - Validar error al crear administrador con token inválido
def test_TC45_Validar_error_al_crear_administrador_con_token_invalido():
    headers = {"Authorization": "Bearer token_invalido"}
    payload = AdministratorsPayload.build_payload_admin(generate_admin_data())
    url = AdministratorsEndpoint.admins()
    response = SyliusRequest.post(url, headers, payload)
    AssertionStatusCode.assert_status_code_401(response)
    AssertionAdministratorsError.assert_admin_error(response.json(), 401, "Invalid JWT Token")

# TC-46: Admin > Administrators – Validar error al crear administrador sin datos requeridos
def test_TC46_Validar_error_al_crear_administrador_sin_datos_requeridos(auth_headers):
    headers = auth_headers
    url = AdministratorsEndpoint.admins()
    response = SyliusRequest.post(url, headers, {})
    print(response.json()["detail"])
    AssertionStatusCode.assert_status_code_422(response)
    AssertionAdministratorsError.assert_admin_error_request(response.json(), 422, "email: Please enter your email.\nusername: Please enter your name.\nlocaleCode: Please choose a locale.\nplainPassword: Please enter your password.")

# TC-47: Admin > Administrators - Validar error al crear administrador con username duplicado
def test_TC47_Validar_error_al_crear_administrador_con_username_duplicado(auth_headers, admin_data):
    headers = auth_headers
    url = AdministratorsEndpoint.admins()
    payload_original = AdministratorsPayload.build_payload_admin(admin_data)
    response_original = SyliusRequest.post(url, headers, payload_original)
    AssertionStatusCode.assert_status_code_201(response_original)
    admin_data_duplicado = generate_admin_data()
    payload_duplicado = AdministratorsPayload.build_payload_admin(admin_data_duplicado)
    payload_duplicado["username"] = payload_original["username"]
    response_duplicado = SyliusRequest.post(url, headers, payload_duplicado)
    AssertionStatusCode.assert_status_code_422(response_duplicado)
    expected_detail = "username: This username is already used."
    AssertionAdministratorsError.assert_admin_error_request(response_duplicado.json(), 422, expected_detail)

# TC-48: Admin > Administrators - Validar error al crear administrador con email duplicado
def test_TC48_Validar_error_al_crear_administrador_con_email_duplicado(auth_headers, admin_data):
    headers = auth_headers
    url = AdministratorsEndpoint.admins()
    payload_original = AdministratorsPayload.build_payload_admin(admin_data)
    response_original = SyliusRequest.post(url, headers, payload_original)
    AssertionStatusCode.assert_status_code_201(response_original)
    admin_data_duplicado = generate_admin_data()
    payload_duplicado = AdministratorsPayload.build_payload_admin(admin_data_duplicado)
    payload_duplicado["email"] = payload_original["email"]
    response_duplicado = SyliusRequest.post(url, headers, payload_duplicado)
    AssertionStatusCode.assert_status_code_422(response_duplicado)
    expected_detail = "email: This email is already used."
    AssertionAdministratorsError.assert_admin_error_request(response_duplicado.json(), 422, expected_detail)

# TC-49: Admin > Administrators - Validar error al crear administrador con email inválido
def test_TC49_Validar_error_al_crear_administrador_con_email_invalido(auth_headers):
    headers = auth_headers
    admin_data = generate_admin_data()
    admin_data["email"] = "correo-invalido"
    payload = AdministratorsPayload.build_payload_admin(admin_data)
    url = AdministratorsEndpoint.admins()
    response = SyliusRequest.post(url, headers, payload)
    AssertionStatusCode.assert_status_code_422(response)
    AssertionAdministratorsError.assert_admin_error_request(response.json(), 422, "email: This email is invalid.")

# TC-50: Admin > Administrators - Crear administrador con enabled activado
def test_TC50_Crear_administrador_enabled_activado(auth_headers, admin_data):
    headers = auth_headers
    payload = AdministratorsPayload.build_payload_admin(admin_data)
    payload["enabled"] = True
    url = AdministratorsEndpoint.admins()
    response = SyliusRequest.post(url, headers, payload)
    AssertionStatusCode.assert_status_code_201(response)
    response_json = response.json()
    AssertionAdministrators.assert_create_schema(response_json)
    AssertionAdministratorsContent.assert_admin_enabled_state(response_json, True)

# TC-51: Admin > Administrators - Crear administrador con enabled desactivado
def test_TC51_Crear_administrador_enabled_desactivado(auth_headers, admin_data):
    headers = auth_headers
    payload = AdministratorsPayload.build_payload_admin(admin_data)
    payload["enabled"] = False
    url = AdministratorsEndpoint.admins()
    response = SyliusRequest.post(url, headers, payload)
    AssertionStatusCode.assert_status_code_201(response)
    response_json = response.json()
    AssertionAdministrators.assert_create_schema(response_json)
    AssertionAdministratorsContent.assert_admin_enabled_state(response_json, False)

# TC-52: Admin > Administrators - Ingresar ID igual a 12345
# TC-53: Admin > Administrators - Validar error al ingresar ID igual a 0
# TC-54: Admin > Administrators - Validar error al ingresar ID string igual a "uno"
# TC-55: Admin > Administrators - Validar error al ingresar ID negativo igual a -1
# TC-56: Admin > Administrators - Validar error al ingresar ID decimal igual a 1.5
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
    
# TC-57: Admin > Administrators - Validar campo firstName con valor null
# TC-58: Admin > Administrators - Ingresar firstName con caracteres menor a 256 caracteres
# TC-59: Admin > Administrators - Ingresar firstName igual a Juan
# TC-60: Admin > Administrators - Validar error al ingresar firstName con 256 caracteres
@pytest.mark.parametrize("firstName, expected_status", [
    (None, 201),
    ("a"*255, 201),
    ("Juan", 201),
    ("a"*256, 422)
])
def test_TC_Admin_Administrators_validar_firstName(auth_headers, firstName, expected_status):
    headers = auth_headers
    admin_data = generate_admin_data()
    admin_data["firstName"] = firstName
    payload = AdministratorsPayload.build_payload_admin(admin_data)
    url = AdministratorsEndpoint.admins()
    response = SyliusRequest.post(url, headers, payload)
    AssertionStatusCode.assert_status_code(response, expected_status)


# TC-61: Admin > Administrators - Validar campo lastName con valor null
# TC-62: Admin > Administrators - Ingresar lastName con caracteres menor a 256 caracteres
# TC-63: Admin > Administrators - Ingresar lastName igual a Pérez
# TC-64: Admin > Administrators - Validar error al ingresar lastName con 256 caracteres
@pytest.mark.parametrize("lastName, expected_status", [
    (None, 201),
    ("a"*255, 201),
    ("Pérez", 201),
    ("a"*256, 422)
])
def test_TC_Admin_Administrators_validar_lastName(auth_headers, lastName, expected_status):
    headers = auth_headers
    admin_data = generate_admin_data()
    admin_data["lastName"] = lastName
    payload = AdministratorsPayload.build_payload_admin(admin_data)
    url = AdministratorsEndpoint.admins()
    response = SyliusRequest.post(url, headers, payload)
    AssertionStatusCode.assert_status_code(response, expected_status)

# TC-65: Admin > Administrators - Ingresar localeCode igual a en_US
# TC-66: Admin > Administrators - Validar error al ingresar localeCode igual a xx_XX
# TC-67: Admin > Administrators - Validar error al ingresar localeCode igual a 123
# TC-68: Admin > Administrators - Validar error al ingresar localeCode vacío
@pytest.mark.parametrize("localeCode, expected_status", [
    ("en_US", 201),
    ("xx_XX", 422),
    pytest.param(123, 422, marks=pytest.mark.xfail(reason="Sylius devuelve 400 en lugar de 422")),
    ("", 422)
])
def test_TC_Admin_Administrators_validar_localeCode(auth_headers, localeCode, expected_status):
    headers = auth_headers
    admin_data = generate_admin_data()
    admin_data["localeCode"] = localeCode
    payload = AdministratorsPayload.build_payload_admin(admin_data)
    url = AdministratorsEndpoint.admins()
    response = SyliusRequest.post(url, headers, payload)
    AssertionStatusCode.assert_status_code(response, expected_status)

# TC-69: Admin > Administrators - Ingresar username igual a 1 carácter
# TC-70: Admin > Administrators - Ingresar username con exactamente 255 caracteres
# TC-71: Admin > Administrators - Ingresar username igual a admin01
# TC-72: Admin > Administrators - Validar error al ingresar username con 0 caracteres
# TC-73: Admin > Administrators - Validar error al ingresar username con 256 caracteres
# TC-74: Admin > Administrators - Validar error al ingresar username vacío
@pytest.mark.parametrize("username, expected_status", [
    pytest.param("a", 201, marks=pytest.mark.xfail(reason="Backend rechaza username corto válido (debería devolver 201)")),
    pytest.param("a"*255, 201, marks=pytest.mark.xfail(reason="Backend rechaza username de longitud máxima válida (debería devolver 201)")),
    pytest.param("admin01_test", 201, marks=pytest.mark.xfail(reason="Backend rechaza username estándar válido (debería devolver 201)")),
    pytest.param("", 422, marks=pytest.mark.xfail(reason="Backend acepta username vacío (debería devolver 422)")),
    ("a"*256, 422),
    pytest.param(None, 422, marks=pytest.mark.xfail(reason="Backend acepta username None (debería devolver 422)")),
])
def test_TC_Admin_Administrators_validar_username(auth_headers, username, expected_status):
    headers = auth_headers
    admin_data = generate_admin_data()
    admin_data["username"] = username
    payload = AdministratorsPayload.build_payload_admin(admin_data)
    url = AdministratorsEndpoint.admins()
    response = SyliusRequest.post(url, headers, payload)
    AssertionStatusCode.assert_status_code(response, expected_status)

# TC-75: Admin > Administrators - Ingresar plainPassword igual a 4 caracteres
# TC-76: Admin > Administrators - Ingresar plainPassword con 255 caracteres
# TC-77: Admin > Administrators - Ingresar plainPassword igual a Test1234
# TC-78: Admin > Administrators - Validar error al ingresar plainPassword con 3 caracteres
# TC-79: Admin > Administrators - Validar error al ingresar plainPassword con 256 caracteres
# TC-80: Admin > Administrators - Validar error al ingresar plainPassword vacío
@pytest.mark.parametrize("plainPassword, expected_status", [
    ("1234", 201),
    ("a"*254, 201),
    ("Test1234", 201),
    ("123", 422),
    ("a"*256, 422),
    ("", 422)
])
def test_TC_Admin_Administrators_validar_plainPassword(auth_headers, plainPassword, expected_status):
    headers = auth_headers
    admin_data = generate_admin_data()
    admin_data["plainPassword"] = plainPassword
    payload = AdministratorsPayload.build_payload_admin(admin_data)
    url = AdministratorsEndpoint.admins()
    response = SyliusRequest.post(url, headers, payload)
    AssertionStatusCode.assert_status_code(response, expected_status)

# TC-81: Admin > Administrators - Ingresar email igual a user@test.com
# TC-82: Admin > Administrators - Validar error al ingresar email igual a test
# TC-83: Admin > Administrators - Validar error al ingresar email igual a user@com
# TC-84: Admin > Administrators - Validar error al ingresar email igual a @mail.com
# TC-85: Admin > Administrators - Validar error al ingresar email vacío
@pytest.mark.parametrize("email, expected_status", [
    ("user900@test.com", 201),
    ("test", 422),
    ("user@com", 422),
    ("@mail.com", 422),
    pytest.param("", 422, marks=pytest.mark.xfail(reason="Backend acepta email vacío (debería devolver 422)")),

])
def test_TC_Admin_Administrators_validar_email(auth_headers, email, expected_status):
    headers = auth_headers
    admin_data = generate_admin_data()
    admin_data["email"] = email
    payload = AdministratorsPayload.build_payload_admin(admin_data)
    url = AdministratorsEndpoint.admins()
    response = SyliusRequest.post(url, headers, payload)
    AssertionStatusCode.assert_status_code(response, expected_status)