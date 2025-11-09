import pytest
import allure
from src.services.request import SyliusRequest
from src.routes.promotions_endpoint import PromotionsEndpoint
from src.assertions.status_code_assertion import AssertionStatusCode
from src.assertions.promotions.schema_assertion import AssertionPromotions
from src.assertions.promotions.error_assertion import AssertionPromotionsError
from src.assertions.promotions.view_content_assertion import AssertionPromotionsContent
from src.data.promotions import generate_promotion_data
from src.resources.payloads.promotions_payload import PromotionsPayload
from src.services.call_request.promotions_call import PromotionsCall

# TC-535: Admin > Marketing > Promotions – Crear promoción con campos válidos
@allure.epic("Módulo de Marketing")
@allure.feature("Promotions")
@allure.story("Creación de promociones")
@allure.title("SYLIUS-535: Crear promoción con campos válidos")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.marketing
@pytest.mark.promotions
@pytest.mark.functional_positive
@pytest.mark.high
def test_TC535_Crear_promocion_campos_validos(auth_headers):
    headers = auth_headers
    payload = PromotionsPayload.build_payload_promotion(generate_promotion_data())
    url = PromotionsEndpoint.promotions()
    response = SyliusRequest.post(url, headers, payload)
    AssertionStatusCode.assert_status_code_201(response)
    response_json = response.json()
    AssertionPromotions.assert_create_schema(response_json)
    AssertionPromotionsContent.assert_promotion_item(response_json, expected_code=payload["code"])

# TC-538: Admin > Marketing > Promotions – Validar error al crear promoción con campos inválidos
@allure.epic("Módulo de Marketing")
@allure.feature("Promotions")
@allure.story("Creación de promociones")
@allure.title("SYLIUS-538: Validar error al crear promoción con campos inválidos")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.marketing
@pytest.mark.promotions
@pytest.mark.functional_negative
@pytest.mark.medium
def test_TC538_Crear_promocion_campos_invalidos(auth_headers):
    headers = auth_headers
    payload = PromotionsPayload.build_invalid_payload()
    url = PromotionsEndpoint.promotions()
    response = SyliusRequest.post(url, headers, payload)
    AssertionStatusCode.assert_status_code(response, 400)
    AssertionPromotionsError.assert_promotion_error(response.json(), 400, "attribute must be")

# TC-540: Admin > Marketing > Promotions – Validar error al crear promoción sin token de autenticación
@allure.epic("Módulo de Marketing")
@allure.feature("Promotions")
@allure.story("Autenticación")
@allure.title("SYLIUS-540: Validar error al crear promoción sin token de autenticación")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.marketing
@pytest.mark.promotions
@pytest.mark.security
@pytest.mark.functional_negative
@pytest.mark.high
def test_TC540_Crear_promocion_sin_token():
    headers = {}
    payload = PromotionsPayload.build_payload_promotion(generate_promotion_data())
    url = PromotionsEndpoint.promotions()
    response = SyliusRequest.post(url, headers, payload)
    AssertionStatusCode.assert_status_code_401(response)
    AssertionPromotionsError.assert_promotion_error(response.json(), 401, "JWT Token not found")

# TC-541: Admin > Marketing > Promotions – Validar error al crear promoción con token inválido
@allure.epic("Módulo de Marketing")
@allure.feature("Promotions")
@allure.story("Autenticación")
@allure.title("SYLIUS-541: Validar error al crear promoción con token inválido")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.marketing
@pytest.mark.promotions
@pytest.mark.security
@pytest.mark.functional_negative
@pytest.mark.high
def test_TC541_Crear_promocion_token_invalido():
    headers = {"Authorization": "Bearer invalid_token"}
    payload = PromotionsPayload.build_payload_promotion(generate_promotion_data())
    url = PromotionsEndpoint.promotions()
    response = SyliusRequest.post(url, headers, payload)
    AssertionStatusCode.assert_status_code_401(response)
    AssertionPromotionsError.assert_promotion_error(response.json(), 401, "Invalid JWT Token")

# TC-536: Admin > Marketing > Promotions – Ingresar code igual a 1 carácter válido
# TC-537: Admin > Marketing > Promotions – Ingresar code con exactamente 255 caracteres
# TC-539: Admin > Marketing > Promotions – Ingresar code con caracteres alfanuméricos y especiales igual a Test_#123/
# TC-542: Admin > Marketing > Promotions – Validar error al ingresar code con 0 caracteres
# TC-543: Admin > Marketing > Promotions – Validar error al ingresar code con 256 caracteres
@allure.epic("Módulo de Marketing")
@allure.feature("Promotions")
@allure.story("Validación de campo 'code'")
@allure.title("SYLIUS-536 - 543: Validar variaciones del parámetro 'code'")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.marketing
@pytest.mark.promotions
@pytest.mark.functional_negative
@pytest.mark.functional_validation
@pytest.mark.functional_edgecase
@pytest.mark.medium
@pytest.mark.parametrize("promo_code, expected_status", [
    ("A", 404),
    ("A" * 255, 404),
    ("Test_#12/", 404),
    pytest.param("", 404, marks=pytest.mark.xfail(reason="Backend devuelve 200 al consultar /promotions/ vacío (debería ser 404)")),
    ("A" * 256, 404)
])
def test_TC_Admin_Promotions_validar_parametros_code(auth_headers, promo_code, expected_status):
    headers = auth_headers
    url = f"{PromotionsEndpoint.promotions()}/{promo_code}"
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code(response, expected_status)

# TC-544: Admin > Marketing > Promotions – Ingresar name igual a 2 carácter válido
# TC-545: Admin > Marketing > Promotions – Ingresar name con exactamente 255 caracteres
# TC-546: Admin > Marketing > Promotions – Ingresar name con caracteres alfanuméricos y especiales igual a Test_#123/
# TC-547: Admin > Marketing > Promotions – Validar error al ingresar name con 1 caracteres
# TC-548: Admin > Marketing > Promotions – Validar error al ingresar name con 256 caracteres
@allure.epic("Módulo de Marketing")
@allure.feature("Promotions")
@allure.story("Validación de campo 'name'")
@allure.title("SYLIUS-544 - 548: Validar variaciones del parámetro 'name'")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.marketing
@pytest.mark.promotions
@pytest.mark.functional_positive
@pytest.mark.functional_validation
@pytest.mark.functional_edgecase
@pytest.mark.medium
@pytest.mark.parametrize("promo_name, expected_status", [
    ("AB", 201),
    ("A" * 255, 201),
    ("Test_#123/", 201),
    ("A", 422),
    ("A" * 256, 422)
])
def test_TC_Admin_Promotions_validar_parametros_name(auth_headers, promo_name, expected_status):
    headers = auth_headers
    base_data = generate_promotion_data()
    payload = PromotionsPayload.build_payload_promotion({**base_data, "name": promo_name})
    url = PromotionsEndpoint.promotions()
    response = SyliusRequest.post(url, headers, payload)
    AssertionStatusCode.assert_status_code(response, expected_status)

# TC-549: Admin > Marketing > Promotions – Ingresar description igual a 2 carácter válido
# TC-550: Admin > Marketing > Promotions – Ingresar description con exactamente 255 caracteres
# TC-551: Admin > Marketing > Promotions – Ingresar description con caracteres alfanuméricos y especiales igual a Test_de_qa/
# TC-552: Admin > Marketing > Promotions – Validar error al ingresar description con 1 caracteres
# TC-553: Admin > Marketing > Promotions – Validar error al ingresar description con 256 caracteres
@allure.epic("Módulo de Marketing")
@allure.feature("Promotions")
@allure.story("Validación de campo 'description'")
@allure.title("SYLIUS-549 - 553: Validar variaciones del parámetro 'description'")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.marketing
@pytest.mark.promotions
@pytest.mark.functional_positive
@pytest.mark.functional_validation
@pytest.mark.functional_edgecase
@pytest.mark.medium
@pytest.mark.parametrize("promo_desc, expected_status", [
    ("AB", 201),
    ("A" * 255, 201),
    ("Test_de_qa/", 201),
    ("A", 422),
    ("A" * 256, 422)
])
def test_TC_Admin_Promotions_validar_parametros_description(auth_headers, promo_desc, expected_status):
    headers = auth_headers
    base_data = generate_promotion_data()
    payload = PromotionsPayload.build_payload_promotion({**base_data, "description": promo_desc })
    url = PromotionsEndpoint.promotions()
    response = SyliusRequest.post(url, headers, payload)
    AssertionStatusCode.assert_status_code(response, expected_status)