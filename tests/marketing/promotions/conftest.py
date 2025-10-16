import pytest
from src.data.promotions import generate_promotion_data
from src.resources.payloads.promotions_payload import PromotionsPayload
from src.services.call_request.promotions_call import PromotionsCall
from src.assertions.status_code_assertion import AssertionStatusCode

@pytest.fixture(scope="module")
def view_promotions(auth_headers):
    payload_promo1 = PromotionsPayload.build_payload_promotion(generate_promotion_data())
    payload_promo2 = PromotionsPayload.build_payload_promotion(generate_promotion_data())
    promo1_response = PromotionsCall.create(auth_headers, payload_promo1)
    promo2_response = PromotionsCall.create(auth_headers, payload_promo2)
    promo1 = promo1_response.json()
    promo2 = promo2_response.json()
    yield auth_headers, promo1, promo2
    PromotionsCall.delete(auth_headers, promo1["code"])
    PromotionsCall.delete(auth_headers, promo2["code"])

@pytest.fixture
def promotion_data():
    return generate_promotion_data()

@pytest.fixture
def create_promotion(auth_headers):
    payload = PromotionsPayload.build_payload_promotion(generate_promotion_data())
    response = PromotionsCall.create(auth_headers, payload)
    AssertionStatusCode.assert_status_code_201(response)
    promo_data = response.json()
    assert "@id" in promo_data, "No se creó correctamente la promoción"
    assert promo_data.get("code") == payload["code"], "El código de promoción no coincide"

    promo_id = promo_data.get("@id").split("/")[-1]
    promo_code = promo_data.get("code")

    yield {
        "headers": auth_headers,
        "promo_id": promo_id,
        "promo_code": promo_code,
        "payload": payload,
        "response": promo_data
    }
    PromotionsCall.delete(auth_headers, promo_code)