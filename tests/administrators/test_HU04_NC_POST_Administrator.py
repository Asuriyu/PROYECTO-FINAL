import pytest
from src.services.request import SyliusRequest
from src.routes.administrators_endpoint import AdministratorsEndpoint
from src.assertions.status_code_assertion import AssertionStatusCode
from src.assertions.administrators.schema_assertion import AssertionAdministrators
from src.assertions.administrators.error_assertion import AssertionAdministratorsError
from src.assertions.administrators.view_content_assertion import AssertionAdministratorsContent
from src.resources.payloads.administrators_payload import AdministratorsPayload
from src.data.administrators import generate_admin_data

# TC-21: Admin > Administrators – Crear administrador con datos válidos
def test_TC21_Crear_administrador_datos_validos(auth_headers, admin_data):
    headers = auth_headers
    payload = AdministratorsPayload.build_payload_admin(admin_data)
    url = AdministratorsEndpoint.admins()
    response = SyliusRequest.post(url, headers, payload)
    AssertionStatusCode.assert_status_code_201(response)
    response_json = response.json()
    AssertionAdministrators.assert_create_schema(response_json)
    AssertionAdministratorsContent.assert_admin_item(response_json, expected_username=payload["username"])

# TC-90: Admin > Administrators – Crear administrador con solo datos requeridos
def test_TC_Admin_Administrators_crear_datos_requeridos(auth_headers):
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

# TC-33: Admin > Administrators - Validar error al crear administrador sin token de autenticación
def test_TC33_Crear_administrador_sin_token():
    headers = {}
    payload = AdministratorsPayload.build_payload_admin(generate_admin_data())
    url = AdministratorsEndpoint.admins()
    response = SyliusRequest.post(url, headers, payload)
    AssertionStatusCode.assert_status_code_401(response)
    AssertionAdministratorsError.assert_admin_error(response.json(), 401, "JWT Token not found")

# TC-34: Admin > Administrators - Validar error al crear administrador con token inválido
def test_TC34_Crear_administrador_token_invalido():
    headers = {"Authorization": "Bearer token_invalido"}
    payload = AdministratorsPayload.build_payload_admin(generate_admin_data())
    url = AdministratorsEndpoint.admins()
    response = SyliusRequest.post(url, headers, payload)
    AssertionStatusCode.assert_status_code_401(response)
    AssertionAdministratorsError.assert_admin_error(response.json(), 401, "Invalid JWT Token")

# TC-296: Admin > Administrators – Validar error al crear administrador sin datos requeridos
def test_TC296_Crear_administrador_sin_datos(auth_headers):
    headers = auth_headers
    url = AdministratorsEndpoint.admins()
    response = SyliusRequest.post(url, headers, {})
    print(response.json()["detail"])
    AssertionStatusCode.assert_status_code_422(response)
    AssertionAdministratorsError.assert_admin_error_request(response.json(), 422, "email: Please enter your email.\nusername: Please enter your name.\nlocaleCode: Please choose a locale.\nplainPassword: Please enter your password.")

# TC-27: Admin > Administrators - Validar error al crear administrador con username duplicado
def test_TC27_Crear_administrador_username_duplicado(auth_headers, admin_data):
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

# TC-28: Admin > Administrators - Validar error al crear administrador con email duplicado
def test_TC28_Crear_administrador_email_duplicado(auth_headers, admin_data):
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
# TC-35: Admin > Administrators - Validar error al crear administrador con email inválido
def test_TC35_Crear_administrador_email_invalido(auth_headers):
    headers = auth_headers
    admin_data = generate_admin_data()
    admin_data["email"] = "correo-invalido"
    payload = AdministratorsPayload.build_payload_admin(admin_data)
    url = AdministratorsEndpoint.admins()
    response = SyliusRequest.post(url, headers, payload)
    AssertionStatusCode.assert_status_code_422(response)
    AssertionAdministratorsError.assert_admin_error_request(response.json(), 422, "email: This email is invalid.")

# TC-31: Admin > Administrators - Crear administrador con enabled activado
def test_TC31_Crear_administrador_enabled_activado(auth_headers, admin_data):
    headers = auth_headers
    payload = AdministratorsPayload.build_payload_admin(admin_data)
    payload["enabled"] = True
    url = AdministratorsEndpoint.admins()
    response = SyliusRequest.post(url, headers, payload)
    AssertionStatusCode.assert_status_code_201(response)
    response_json = response.json()
    AssertionAdministrators.assert_create_schema(response_json)
    AssertionAdministratorsContent.assert_admin_enabled_state(response_json, True)

# TC-496: Admin > Administrators - Crear administrador con enabled desactivado
def test_TC496_Crear_administrador_enabled_desactivado(auth_headers, admin_data):
    headers = auth_headers
    payload = AdministratorsPayload.build_payload_admin(admin_data)
    payload["enabled"] = False
    url = AdministratorsEndpoint.admins()
    response = SyliusRequest.post(url, headers, payload)
    AssertionStatusCode.assert_status_code_201(response)
    response_json = response.json()
    AssertionAdministrators.assert_create_schema(response_json)
    AssertionAdministratorsContent.assert_admin_enabled_state(response_json, False)

# TC-474: Admin > Administrators - Ingresar ID igual a 12345
# TC-475: Admin > Administrators - Validar error al ingresar ID igual a 0
# TC-476: Admin > Administrators - Validar error al ingresar ID string igual a "uno"
# TC-477: Admin > Administrators - Validar error al ingresar ID negativo igual a -1
# TC-478: Admin > Administrators - Validar error al ingresar ID decimal igual a 1.5
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
    
# TC-538: Admin > Administrators - Validar campo firstName con valor null
# TC-539: Admin > Administrators - Ingresar firstName con caracteres menor a 256 caracteres
# TC-540: Admin > Administrators - Ingresar firstName igual a Juan
# TC-541: Admin > Administrators - Validar error al ingresar firstName con 256 caracteres
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


# TC-542: Admin > Administrators - Validar campo lastName con valor null
# TC-543: Admin > Administrators - Ingresar lastName con caracteres menor a 256 caracteres
# TC-544: Admin > Administrators - Ingresar lastName igual a Pérez
# TC-545: Admin > Administrators - Validar error al ingresar lastName con 256 caracteres

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

# TC-546: Admin > Administrators - Ingresar localeCode igual a en_US
# TC-547: Admin > Administrators - Validar error al ingresar localeCode igual a xx_XX
# TC-548: Admin > Administrators - Validar error al ingresar localeCode igual a 123
# TC-549: Admin > Administrators - Validar error al ingresar localeCode vacío

@pytest.mark.parametrize("localeCode, expected_status", [
    ("en_US", 201),
    ("xx_XX", 422),
    (123, 422),
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

# TC-550: Admin > Administrators - Ingresar username igual a 1 carácter
# TC-551: Admin > Administrators - Ingresar username con exactamente 255 caracteres
# TC-552: Admin > Administrators - Ingresar username igual a admin01
# TC-553: Admin > Administrators - Validar error al ingresar username con 0 caracteres
# TC-554: Admin > Administrators - Validar error al ingresar username con 256 caracteres
# TC-555: Admin > Administrators - Validar error al ingresar username vacío

@pytest.mark.parametrize("username, expected_status", [
    ("a", 201),
    ("a"*255, 201),
    ("admin01_test", 201),
    ("", 422),
    ("a"*256, 422),
    (None, 422)
])
def test_TC_Admin_Administrators_validar_username(auth_headers, username, expected_status):
    headers = auth_headers
    admin_data = generate_admin_data()
    admin_data["username"] = username
    payload = AdministratorsPayload.build_payload_admin(admin_data)
    url = AdministratorsEndpoint.admins()
    response = SyliusRequest.post(url, headers, payload)
    AssertionStatusCode.assert_status_code(response, expected_status)

# TC-556: Admin > Administrators - Ingresar plainPassword igual a 4 caracteres
# TC-557: Admin > Administrators - Ingresar plainPassword con 255 caracteres
# TC-558: Admin > Administrators - Ingresar plainPassword igual a Test1234
# TC-559: Admin > Administrators - Validar error al ingresar plainPassword con 3 caracteres
# TC-560: Admin > Administrators - Validar error al ingresar plainPassword con 256 caracteres
# TC-561: Admin > Administrators - Validar error al ingresar plainPassword vacío

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

# TC-562: Admin > Administrators - Ingresar email igual a user@test.com
# TC-563: Admin > Administrators - Validar error al ingresar email igual a test
# TC-564: Admin > Administrators - Validar error al ingresar email igual a user@com
# TC-565: Admin > Administrators - Validar error al ingresar email igual a @mail.com
# TC-566: Admin > Administrators - Validar error al ingresar email vacío

@pytest.mark.parametrize("email, expected_status", [
    ("user1@test.com", 201),
    ("test", 422),
    ("user@com", 422),
    ("@mail.com", 422),
    ("", 422)
])
def test_TC_Admin_Administrators_validar_email(auth_headers, email, expected_status):
    headers = auth_headers
    admin_data = generate_admin_data()
    admin_data["email"] = email
    payload = AdministratorsPayload.build_payload_admin(admin_data)
    url = AdministratorsEndpoint.admins()
    response = SyliusRequest.post(url, headers, payload)
    AssertionStatusCode.assert_status_code(response, expected_status)
