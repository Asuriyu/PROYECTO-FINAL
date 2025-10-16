import pytest
from src.data.promotions import generate_promotion_data
from src.resources.payloads.promotions_payload import PromotionsPayload
from src.services.call_request.promotions_call import PromotionsCall


@pytest.fixture(scope="module")
def view_promotions(auth_headers):
    """Crea dos promociones de ejemplo antes de los tests y las elimina al finalizar."""
    payload_promo1 = PromotionsPayload.build_payload_promotion(generate_promotion_data())
    payload_promo2 = PromotionsPayload.build_payload_promotion(generate_promotion_data())
    promo1 = PromotionsCall.create(auth_headers, payload_promo1)
    promo2 = PromotionsCall.create(auth_headers, payload_promo2)

    yield auth_headers, promo1, promo2

    PromotionsCall.delete(auth_headers, promo1["code"])
    PromotionsCall.delete(auth_headers, promo2["code"])


@pytest.fixture
def promotion_data():
    return generate_promotion_data()