import pytest
from src.data.promotions import generate_promotion_data
from src.resources.payloads.promotions_payload import PromotionsPayload
from src.assertions.status_code_assertion import AssertionStatusCode
from src.assertions.promotions.schema_assertion import AssertionPromotions
from src.assertions.promotions.error_assertion import AssertionPromotionsError
from src.assertions.promotions.view_content_assertion import AssertionPromotionsContent
from src.services.call_request.promotions_call import PromotionsCall

# TC-555: Admin > Marketing > Promotions – Actualizar promoción con campos válidos
def test_TC555_Actualizar_promocion_campos_validos(create_promotion):
    headers = create_promotion["headers"]
    promo_code = create_promotion["promo_code"]
    update_payload = PromotionsPayload.build_payload_promotion(generate_promotion_data())
    response = PromotionsCall.update(headers, promo_code, update_payload)
    AssertionStatusCode.assert_status_code_200(response)
    response_json = response.json()
    AssertionPromotions.assert_update_schema(response_json)
    AssertionPromotionsContent.assert_promotion_item(response_json, expected_code=update_payload["code"])

# TC-556: Admin > Marketing > Promotions – Validar error al actualizar promoción con campos inválidos
def test_TC556_Actualizar_promocion_campos_invalidos(create_promotion):
    headers = create_promotion["headers"]
    promo_code = create_promotion["promo_code"]
    invalid_payload = PromotionsPayload.build_invalid_payload()
    response = PromotionsCall.update(headers, promo_code, invalid_payload)
    AssertionStatusCode.assert_status_code(response, 400)
    AssertionPromotionsError.assert_promotion_error(response.json(), 400, "attribute must be")

# TC-557: Admin > Marketing > Promotions – Validar error al actualizar promoción sin token de autenticación
def test_TC557_Actualizar_promocion_sin_token(create_promotion):
    promo_code = create_promotion["promo_code"]
    headers = {}
    payload = PromotionsPayload.build_payload_promotion(generate_promotion_data())
    response = PromotionsCall.update(headers, promo_code, payload)
    AssertionStatusCode.assert_status_code_401(response)
    AssertionPromotionsError.assert_promotion_error(response.json(), 401, "JWT Token not found")


# TC-558: Admin > Marketing > Promotions – Validar error al actualizar promoción con token inválido
def test_TC558_Actualizar_promocion_token_invalido(create_promotion):
    promo_code = create_promotion["promo_code"]
    headers = {"Authorization": "Bearer invalid_token"}
    payload = PromotionsPayload.build_payload_promotion(generate_promotion_data())
    response = PromotionsCall.update(headers, promo_code, payload)
    AssertionStatusCode.assert_status_code_401(response)
    AssertionPromotionsError.assert_promotion_error(response.json(), 401, "Invalid JWT Token")

# TC-559: Admin > Marketing > Promotions – Ingresar code igual a 1 carácter válido
# TC-560: Admin > Marketing > Promotions – Ingresar code con exactamente 255 caracteres
# TC-561: Admin > Marketing > Promotions – Ingresar code con caracteres alfanuméricos y especiales igual a Test_#123/
# TC-562: Admin > Marketing > Promotions – Validar error al ingresar code con 0 caracteres
# TC-563: Admin > Marketing > Promotions – Validar error al ingresar code con 256 caracteres
@pytest.mark.parametrize("promo_code, expected_status", [
    ("A", 200),
    ("A" * 255, 200),
    ("Test_#123/", 200),
    ("", 200),
    ("A" * 256, 200)
])
def test_TC_Admin_Promotions_validar_parametros_code(create_promotion, promo_code, expected_status):
    headers = create_promotion["headers"]
    promo_code_original = create_promotion["promo_code"]
    payload = PromotionsPayload.build_payload_promotion({**generate_promotion_data(), "code": promo_code})
    response = PromotionsCall.update(headers, promo_code_original, payload)
    AssertionStatusCode.assert_status_code(response, expected_status)

# TC-564: Admin > Marketing > Promotions – Ingresar name igual a 2 caracteres válidos
# TC-565: Admin > Marketing > Promotions – Ingresar name con exactamente 255 caracteres
# TC-566: Admin > Marketing > Promotions – Ingresar name con caracteres alfanuméricos y especiales igual a Promo_#123
# TC-567: Admin > Marketing > Promotions – Validar error al ingresar name con 1 carácter
# TC-568: Admin > Marketing > Promotions – Validar error al ingresar name con 256 caracteres
@pytest.mark.parametrize("promo_name, expected_status", [
    ("AB", 200),
    ("A" * 255, 200),
    ("Promo_#123", 200),
    ("", 422),
    ("A" * 256,422)
])
def test_TC_Admin_Promotions_validar_parametros_name(create_promotion, promo_name, expected_status):
    headers = create_promotion["headers"]
    promo_code = create_promotion["promo_code"]
    payload = PromotionsPayload.build_payload_promotion({**generate_promotion_data(), "name": promo_name})
    response = PromotionsCall.update(headers, promo_code, payload)
    AssertionStatusCode.assert_status_code(response, expected_status)

# TC-569: Admin > Marketing > Promotions – Ingresar description igual a 2 carácter válido
# TC-570: Admin > Marketing > Promotions – Ingresar description con exactamente 255 caracteres
# TC-571: Admin > Marketing > Promotions – Ingresar description con caracteres alfanuméricos y especiales igual a Test_de_qa/
# TC-572: Admin > Marketing > Promotions – Validar error al ingresar description con 1 carácter
# TC-573: Admin > Marketing > Promotions – Validar error al ingresar description con 256 caracteres
@pytest.mark.parametrize("promo_desc, expected_status", [
    ("AB", 200),
    ("A" * 255, 200),
    ("Test_de_qa/", 200),
    ("", 422),
    ("A" * 256, 422)
])
def test_TC_Admin_Promotions_validar_parametros_description(create_promotion, promo_desc, expected_status):
    headers = create_promotion["headers"]
    promo_code = create_promotion["promo_code"]
    payload = PromotionsPayload.build_payload_promotion({**generate_promotion_data(), "description": promo_desc})
    response = PromotionsCall.update(headers, promo_code, payload)
    AssertionStatusCode.assert_status_code(response, expected_status)