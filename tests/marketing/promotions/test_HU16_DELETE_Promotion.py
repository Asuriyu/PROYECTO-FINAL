import pytest
from src.services.request import SyliusRequest
from src.routes.promotions_endpoint import PromotionsEndpoint
from src.assertions.status_code_assertion import AssertionStatusCode
from src.assertions.promotions.schema_assertion import AssertionPromotions
from src.assertions.promotions.error_assertion import AssertionPromotionsError
from src.services.call_request.promotions_call import PromotionsCall

# TC-516: Admin > Marketing > Promotions – Eliminar promoción existente con code válido
def test_TC516_Eliminar_promocion_code_valido(create_promotion):
    headers = create_promotion["headers"]
    promo_code = create_promotion["promo_code"]
    response = PromotionsCall.delete(headers, promo_code)
    AssertionStatusCode.assert_status_code_204(response)

# TC-517: Admin > Marketing > Promotions – Validar error al eliminar promoción inexistente
def test_TC517_Eliminar_promocion_inexistente(auth_headers):
    headers = auth_headers
    fake_code = "PROMONOTFOUND"
    response = PromotionsCall.delete(headers, fake_code)
    AssertionStatusCode.assert_status_code(response, 404)
    AssertionPromotionsError.assert_promotion_error(response.json(), 404, "Promotion not found")

# TC-518: Admin > Marketing > Promotions – Validar error al eliminar promoción sin token de autenticación
def test_TC518_Eliminar_promocion_sin_token():
    headers = {}
    fake_code = "PROMOFAKE"
    response = SyliusRequest.delete(f"{PromotionsEndpoint.promotions()}/{fake_code}", headers)
    AssertionStatusCode.assert_status_code(response, 401)
    AssertionPromotionsError.assert_promotion_error(response.json(), 401, "JWT Token not found")

# TC-519: Admin > Marketing > Promotions – Validar error al eliminar promoción con token inválido
def test_TC519_Eliminar_promocion_token_invalido():
    headers = {"Authorization": "Bearer invalid_token"}
    fake_code = "PROMOFAKE"
    response = SyliusRequest.delete(f"{PromotionsEndpoint.promotions()}/{fake_code}", headers)
    AssertionStatusCode.assert_status_code(response, 401)
    AssertionPromotionsError.assert_promotion_error(response.json(), 401, "Invalid JWT Token")

# TC-520: Admin > Marketing > Promotions – Verificar eliminación de promoción deshabilitada o archivada
def test_TC520_Eliminar_promocion_archivada(create_promotion):
    headers = create_promotion["headers"]
    promo_code = create_promotion["promo_code"]
    archive_response = PromotionsCall.archive(headers, promo_code)
    AssertionStatusCode.assert_status_code_200(archive_response)
    delete_response = PromotionsCall.delete(headers, promo_code)
    AssertionStatusCode.assert_status_code_204(delete_response)

# TC-521: Admin > Marketing > Promotions – Validar error al eliminar promoción repetida
def test_TC521_Eliminar_promocion_repetida(create_promotion):
    headers = create_promotion["headers"]
    promo_code = create_promotion["promo_code"]
    first_response = PromotionsCall.delete(headers, promo_code)
    AssertionStatusCode.assert_status_code_204(first_response)
    second_response = PromotionsCall.delete(headers, promo_code)
    AssertionStatusCode.assert_status_code(second_response, 404)
    AssertionPromotionsError.assert_promotion_error(second_response.json(), 404, "Promotion not found")

# TC-522: Admin > Marketing > Promotions – Verificar eliminación concurrente de la misma promoción
def test_TC522_Eliminar_promocion_concurrente(create_promotion):
    headers = create_promotion["headers"]
    promo_code = create_promotion["promo_code"]
    response1 = PromotionsCall.delete(headers, promo_code)
    response2 = PromotionsCall.delete(headers, promo_code)
    statuses = sorted([response1.status_code, response2.status_code])
    assert statuses == [204, 404], f"Resultados inesperados: {statuses}"

# TC-523: Admin > Marketing > Promotions – Verificar que una promoción eliminada no exista más en el sistema
def test_TC523_Eliminar_promocion_verificar_inexistencia(create_promotion):
    headers = create_promotion["headers"]
    promo_code = create_promotion["promo_code"]
    delete_response = PromotionsCall.delete(headers, promo_code)
    AssertionStatusCode.assert_status_code_204(delete_response)
    get_response = SyliusRequest.get(f"{PromotionsEndpoint.promotions()}/{promo_code}", headers)
    AssertionStatusCode.assert_status_code(get_response, 404)
    AssertionPromotionsError.assert_promotion_error(get_response.json(), 404, "Promotion not found")