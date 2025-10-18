import pytest
from src.services.request import SyliusRequest
from src.routes.promotions_endpoint import PromotionsEndpoint
from src.assertions.status_code_assertion import AssertionStatusCode
from src.assertions.promotions.schema_assertion import AssertionPromotions
from src.assertions.promotions.error_assertion import AssertionPromotionsError
from src.assertions.promotions.view_content_assertion import AssertionPromotionsContent
from src.data.promotions import generate_promotion_data
from src.resources.payloads.promotions_payload import PromotionsPayload
from src.services.call_request.promotions_call import PromotionsCall

# TC-529: Admin > Marketing > Promotions – Archivar promoción existente con code válido
def test_TC529_Archivar_promocion_code_valido(create_promotion):
    headers = create_promotion["headers"]
    promo_code = create_promotion["promo_code"]
    response = PromotionsCall.archive(headers, promo_code)
    AssertionStatusCode.assert_status_code_200(response)
    response_json = response.json()
    AssertionPromotions.assert_update_schema(response_json)
    AssertionPromotionsContent.assert_promotion_item(response_json, expected_code=promo_code)

# TC-530: Admin > Marketing > Promotions – Validar error al archivar promoción sin token de autenticación
def test_TC530_Archivar_promocion_sin_token():
    headers = {}
    fake_code = "PROMOFAKE"
    response = SyliusRequest.patch(f"{PromotionsEndpoint.promotions()}/{fake_code}/archive", headers)
    AssertionStatusCode.assert_status_code(response, 401)
    AssertionPromotionsError.assert_promotion_error(response.json(), 401, "JWT Token not found")

# TC-531: Admin > Marketing > Promotions – Validar error al archivar promoción con token inválido
def test_TC531_Archivar_promocion_token_invalido():
    headers = {"Authorization": "Bearer invalid_token"}
    fake_code = "PROMOFAKE"
    response = SyliusRequest.patch(f"{PromotionsEndpoint.promotions()}/{fake_code}/archive", headers)
    AssertionStatusCode.assert_status_code(response, 401)
    AssertionPromotionsError.assert_promotion_error(response.json(), 401, "Invalid JWT Token")

# TC-532: Admin > Marketing > Promotions – Validar error al archivar promoción inexistente
def test_TC532_Archivar_promocion_inexistente(auth_headers):
    headers = auth_headers
    non_existing_code = "PROMONOTFOUND"
    response = PromotionsCall.archive(headers, non_existing_code)
    AssertionStatusCode.assert_status_code(response, 404)
    AssertionPromotionsError.assert_promotion_error(response.json(), 404, "Promotion not found")

# TC-533: Admin > Marketing > Promotions – Validar comportamiento al archivar promoción ya archivada previamente
def test_TC533_Archivar_promocion_ya_archivada(create_promotion):
    headers = create_promotion["headers"]
    promo_code = create_promotion["promo_code"]
    first_response = PromotionsCall.archive(headers, promo_code)
    AssertionStatusCode.assert_status_code_200(first_response)
    second_response = PromotionsCall.archive(headers, promo_code)
    AssertionStatusCode.assert_status_code_200(second_response)
    response_json = second_response.json()
    AssertionPromotions.assert_update_schema(response_json)
    AssertionPromotionsContent.assert_promotion_item(response_json, expected_code=promo_code)