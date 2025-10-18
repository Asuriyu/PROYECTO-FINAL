import pytest
from src.routes.endpoint import Endpoint
from src.services.request import SyliusRequest
from src.assertions.status_code_assertion import AssertionStatusCode
from src.assertions.login.schema_assertion import AssertionLogin
from src.assertions.login.error_assertion import AssertionLoginError
from src.utils.logger_helpers import log_request_response


# TC-91: Admin > Login - Autenticación exitosa con email y contraseña válidos
# TC-102: Admin > Login - Autenticación exitosa con email en mayúsculas
@pytest.mark.parametrize("email, password", [
    ("api@example.com","sylius-api"),
    ("API@EXAMPLE.COM","sylius-api")
])
def test_TC_91_Autenticacion_exitosa_con_email_y_contrasena_validos(email, password):
    payload = {"email": email, "password": password}
    url = Endpoint.login()
    response = SyliusRequest.post(url, payload=payload)
    log_request_response("POST", url, response, payload=payload)
    AssertionLogin.assert_input_schema(payload)
    AssertionStatusCode.assert_status_code_200(response)
    AssertionLogin.assert_output_schema(response.json())


# TC-92: Admin > Login - Autenticación fallida con email y contraseña inválidos
# TC-93: Admin > Login - Autenticación fallida con email inválido y contraseña válida
# TC-94: Admin > Login - Autenticación fallida con email válido y contraseña inválida
# TC-103: Admin > Login - Autenticación fallida con contraseña en mayúsculas
# TC-104: Admin > Login - Autenticación fallida con email con espacios al inicio y fin
# TC-105: Admin > Login - Autenticación fallida con contraseña con espacios al inicio y fin
@pytest.mark.parametrize("email, password", [
    ("asdfSDFs23d","SFhgsf23"),
    ("asdfSDFs23d","sylius-api"),
    ("api@example.com","SFhgsf23"),
    ("api@example.com","SYLIUS-API"),
    (" api@example.com ","sylius-api"),
    ("api@example.com"," sylius-api ")
])
def test_TC_Autenticacion_fallida_401(email, password):
    payload = {"email": email, "password": password}
    url = Endpoint.login()
    response = SyliusRequest.post(url, payload=payload)
    log_request_response("POST", url, response, payload=payload)
    AssertionStatusCode.assert_status_code_401(response)
    AssertionLoginError.assert_login_error(response.json(), 401, "Invalid credentials.")


# TC-95: Admin > Login - Autenticación fallida con email vacío
# TC-96: Admin > Login - Autenticación fallida con contraseña vacío
# TC-97: Admin > Login - Autenticación fallida con email y contraseña vacíos
# TC-98: Admin > Login - Autenticación fallida sin el campo email
# TC-99: Admin > Login - Autenticación fallida sin el campo contraseña
# TC-100: Admin > Login - Autenticación fallida con body vacío
# TC-101: Admin > Login - Autenticación fallida sin enviar body
@pytest.mark.parametrize("payload", [
    {"email": "", "password": "sylius-api"},
    {"email": "api@example.com", "password": ""},
    {"email": "", "password": ""},
    {"password": "sylius-api"},
    {"email": "api@example.com"},
    {},
    None                                          
])
def test_TC_Autenticacion_fallida_400(payload):
    url = Endpoint.login()
    if payload is None:
        response = SyliusRequest.post(url)
    else:
        response = SyliusRequest.post(url, payload=payload)
    log_request_response("POST", url, response, payload=payload)
    AssertionStatusCode.assert_status_code_400(response)
    AssertionLoginError.assert_login_error(response.json(), 400, "Bad Request")