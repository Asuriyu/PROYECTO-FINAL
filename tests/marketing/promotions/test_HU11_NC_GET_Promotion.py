import pytest
import allure
from src.services.request import SyliusRequest
from src.routes.promotions_endpoint import PromotionsEndpoint
from src.assertions.status_code_assertion import AssertionStatusCode
from src.assertions.promotions.schema_assertion import AssertionPromotions
from src.assertions.promotions.error_assertion import AssertionPromotionsError
from src.assertions.promotions.view_content_assertion import AssertionPromotionsContent

# TC-506: Admin > Marketing > Promotions – Validar error al consultar una promoción sin token de autenticación
@allure.epic("Módulo de Marketing")
@allure.feature("Promotions")
@allure.story("Consulta individual de promoción")
@allure.title("SYLIUS-506: Validar error al consultar una promoción sin token de autenticación")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.marketing
@pytest.mark.promotions
@pytest.mark.security
@pytest.mark.functional_negative
@pytest.mark.high
def test_TC506_Consultar_promocion_sin_token():
    headers = {}
    promo_code = "PROMO123"
    url = f"{PromotionsEndpoint.promotions()}/{promo_code}"
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_401(response)
    AssertionPromotionsError.assert_promotion_error(response.json(), 401, "JWT Token not found")

# TC-507: Admin > Marketing > Promotions – Validar error al consultar una promoción con token inválido
@allure.epic("Módulo de Marketing")
@allure.feature("Promotions")
@allure.story("Consulta individual de promoción")
@allure.title("SYLIUS-507: Validar error al consultar una promoción con token inválido")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.marketing
@pytest.mark.promotions
@pytest.mark.security
@pytest.mark.functional_negative
@pytest.mark.high
def test_TC507_Consultar_promocion_token_invalido():
    headers = {"Authorization": "Bearer invalid_token"}
    promo_code = "PROMO123"
    url = f"{PromotionsEndpoint.promotions()}/{promo_code}"
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_401(response)
    AssertionPromotionsError.assert_promotion_error(response.json(), 401, "Invalid JWT Token")

# TC-508: Admin > Marketing > Promotions – Validar códigos únicos de promociones
@allure.epic("Módulo de Marketing")
@allure.feature("Promotions")
@allure.story("Validación de unicidad de códigos")
@allure.title("SYLIUS-508: Validar códigos únicos de promociones")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.marketing
@pytest.mark.promotions
@pytest.mark.functional_positive
@pytest.mark.functional_validation
@pytest.mark.medium
def test_TC508_Validar_codigos_unicos_promociones(view_promotions):
    headers, _, _ = view_promotions
    url = PromotionsEndpoint.promotions()
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_200(response)
    response_json = response.json()
    AssertionPromotions.assert_list_schema(response_json)
    members = response_json.get("hydra:member", [])
    codes = [promo.get("code") for promo in members if "code" in promo]
    assert len(codes) == len(set(codes)), f"Los códigos de promociones no son únicos: {codes}"


# TC-509: Admin > Marketing > Promotions – Verificar localización consistente de los datos
@allure.epic("Módulo de Marketing")
@allure.feature("Promotions")
@allure.story("Validación de consistencia de localización")
@allure.title("SYLIUS-509: Verificar localización consistente de los datos de promociones")
@allure.severity(allure.severity_level.TRIVIAL)
@pytest.mark.marketing
@pytest.mark.promotions
@pytest.mark.functional_positive
@pytest.mark.functional_validation
@pytest.mark.low
def test_TC509_Verificar_localizacion_consistente(view_promotions):
    headers, _, _ = view_promotions
    url = PromotionsEndpoint.promotions()
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_200(response)
    response_json = response.json()
    AssertionPromotions.assert_list_schema(response_json)
    members = response_json.get("hydra:member", [])
    locales = [promo.get("translations") for promo in members if "translations" in promo]
    assert all(isinstance(loc, dict) for loc in locales), "Formato inválido en translations"
    assert all(len(loc) > 0 for loc in locales), "Existen promociones sin datos de traducción"

# TC-510: Admin > Marketing > Promotions – Obtener promoción activa
@allure.epic("Módulo de Marketing")
@allure.feature("Promotions")
@allure.story("Consulta de promociones activas")
@allure.title("SYLIUS-510: Obtener promoción activa")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.marketing
@pytest.mark.promotions
@pytest.mark.functional_positive
@pytest.mark.medium
def test_TC510_Obtener_promocion_activa(view_promotions):
    headers, _, _ = view_promotions
    url = PromotionsEndpoint.promotions_with_params(enabled=True)
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_200(response)
    response_json = response.json()
    AssertionPromotions.assert_list_schema(response_json)
    AssertionPromotionsContent.assert_promotion_collection(response_json, params={"enabled": True})

# TC-511: Admin > Marketing > Promotions – Ingresar code igual a 1 carácter válido  
# TC-512: Admin > Marketing > Promotions – Ingresar code con exactamente 255 caracteres  
# TC-513: Admin > Marketing > Promotions – Ingresar code con caracteres alfanuméricos y especiales igual a Test_#12/  
# TC-514: Admin > Marketing > Promotions – Validar error al ingresar code con 0 caracteres  
# TC-515: Admin > Marketing > Promotions – Validar error al ingresar code con 256 caracteres  
@allure.epic("Módulo de Marketing")
@allure.feature("Promotions")
@allure.story("Validación del parámetro 'code'")
@allure.title("SYLIUS-511 - 515: Validar parámetros del campo code")
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
    ("", 200),                       
    ("A" * 256, 404)                   
])
def test_TC_Admin_Promotions_validar_parametros_code(auth_headers, promo_code, expected_status):
    headers = auth_headers
    url = f"{PromotionsEndpoint.promotions()}/{promo_code}"
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code(response, expected_status)
    response_json = response.json()