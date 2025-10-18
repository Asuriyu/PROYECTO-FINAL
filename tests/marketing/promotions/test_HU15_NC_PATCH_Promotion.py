import pytest
from src.services.request import SyliusRequest
from src.routes.promotions_endpoint import PromotionsEndpoint
from src.assertions.status_code_assertion import AssertionStatusCode
from src.assertions.promotions.schema_assertion import AssertionPromotions
from src.assertions.promotions.error_assertion import AssertionPromotionsError
from src.assertions.promotions.view_content_assertion import AssertionPromotionsContent
from src.services.call_request.promotions_call import PromotionsCall

# TC-524: Admin > Marketing > Promotions – Restaurar promoción previamente archivada con code válido
def test_TC524_Restaurar_promocion_code_valido(create_promotion):
    headers = create_promotion["headers"]
    promo_code = create_promotion["promo_code"]
    archive_response = PromotionsCall.archive(headers, promo_code)
    AssertionStatusCode.assert_status_code_200(archive_response)
    restore_response = PromotionsCall.restore(headers, promo_code)
    AssertionStatusCode.assert_status_code_200(restore_response)
    response_json = restore_response.json()
    AssertionPromotions.assert_update_schema(response_json)
    AssertionPromotionsContent.assert_promotion_item(response_json, expected_code=promo_code)

# TC-525: Admin > Marketing > Promotions – Validar error al restaurar promoción sin token de autenticación
def test_TC525_Restaurar_promocion_sin_token():
    headers = {}
    fake_code = "PROMOFAKE"
    response = SyliusRequest.patch(f"{PromotionsEndpoint.promotions()}/{fake_code}/restore", headers)
    AssertionStatusCode.assert_status_code(response, 401)
    AssertionPromotionsError.assert_promotion_error(response.json(), 401, "JWT Token not found")

# TC-526: Admin > Marketing > Promotions – Validar error al restaurar promoción con token inválido
def test_TC526_Restaurar_promocion_token_invalido():
    headers = {"Authorization": "Bearer invalid_token"}
    fake_code = "PROMOFAKE"
    response = SyliusRequest.patch(f"{PromotionsEndpoint.promotions()}/{fake_code}/restore", headers)
    AssertionStatusCode.assert_status_code(response, 401)
    AssertionPromotionsError.assert_promotion_error(response.json(), 401, "Invalid JWT Token")

# TC-527: Admin > Marketing > Promotions – Validar comportamiento al restaurar promoción no archivada
def test_TC527_Restaurar_promocion_no_archivada(create_promotion):
    headers = create_promotion["headers"]
    promo_code = create_promotion["promo_code"]
    response = PromotionsCall.restore(headers, promo_code)
    AssertionStatusCode.assert_status_code_200(response)
    response_json = response.json()
    AssertionPromotions.assert_update_schema(response_json)
    AssertionPromotionsContent.assert_promotion_item(response_json, expected_code=promo_code)

# TC-528: Admin > Marketing > Promotions – Validar error al restaurar promoción inexistente
def test_TC528_Restaurar_promocion_inexistente(auth_headers):
    headers = auth_headers
    fake_code = "PROMONOTFOUND"
    response = PromotionsCall.restore(headers, fake_code)
    AssertionStatusCode.assert_status_code(response, 404)
    AssertionPromotionsError.assert_promotion_error(response.json(), 404, "Promotion not found")