import pytest
import allure
from src.services.request import SyliusRequest
from src.routes.product_reviews_endpoint import ProductReviewsEndpoint
from src.assertions.status_code_assertion import AssertionStatusCode
from src.assertions.product_reviews.error_assertion import AssertionProductReviewsError
from src.services.call_request.product_reviews_call import ProductReviewsCall

# TC-575: Admin > Marketing > Product Reviews – Eliminar review existente con ID válido
@allure.epic("Módulo de Marketing")
@allure.feature("Product Reviews")
@allure.story("Eliminar reseña de producto")
@allure.title("SYLIUS-575: Eliminar review existente con ID válido")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.marketing
@pytest.mark.product_reviews
@pytest.mark.functional_positive
@pytest.mark.high
def test_TC575_Eliminar_review_existente_valido(create_product_review):
    headers = create_product_review["headers"]
    review_id = create_product_review["review_id"]
    response = ProductReviewsCall.delete(headers, review_id)
    AssertionStatusCode.assert_status_code_204(response)
    follow_up = ProductReviewsCall.get_by_id(headers, review_id)
    AssertionStatusCode.assert_status_code(follow_up, 404)

# TC-576: Admin > Marketing > Product Reviews – Validar error al eliminar review inexistente
@allure.epic("Módulo de Marketing")
@allure.feature("Product Reviews")
@allure.story("Eliminar reseña de producto")
@allure.title("SYLIUS-576: Validar error al eliminar review inexistente")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.marketing
@pytest.mark.product_reviews
@pytest.mark.functional_negative
@pytest.mark.medium
def test_TC576_Eliminar_review_inexistente(auth_headers):
    headers = auth_headers
    fake_id = "999999"
    response = ProductReviewsCall.delete(headers, fake_id)
    AssertionStatusCode.assert_status_code(response, 404)
    AssertionProductReviewsError.assert_review_error( response.json(), expected_code=404, expected_message="Product review not found")

# TC-577: Admin > Marketing > Product Reviews – Validar error al eliminar review sin autenticación
@allure.epic("Módulo de Marketing")
@allure.feature("Product Reviews")
@allure.story("Eliminar reseña de producto")
@allure.title("SYLIUS-577: Validar error al eliminar review sin token de autenticación")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.marketing
@pytest.mark.product_reviews
@pytest.mark.security
@pytest.mark.functional_negative
@pytest.mark.high
def test_TC577_Eliminar_review_sin_token():
    headers = {}
    fake_id = "999999"
    response = SyliusRequest.delete(f"{ProductReviewsEndpoint.product_review_id(fake_id)}", headers)
    AssertionStatusCode.assert_status_code(response, 401)
    AssertionProductReviewsError.assert_review_error(response.json(), 401, "JWT Token not found")

# TC-578: Admin > Marketing > Product Reviews – Validar error al eliminar review con token inválido
@allure.epic("Módulo de Marketing")
@allure.feature("Product Reviews")
@allure.story("Eliminar reseña de producto")
@allure.title("SYLIUS-578: Validar error al eliminar review con token inválido")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.marketing
@pytest.mark.product_reviews
@pytest.mark.security
@pytest.mark.functional_negative
@pytest.mark.high
def test_TC578_Eliminar_review_token_invalido():
    headers = {"Authorization": "Bearer invalid_token"}
    fake_id = "999999"
    response = SyliusRequest.delete(f"{ProductReviewsEndpoint.product_review_id(fake_id)}", headers)
    AssertionStatusCode.assert_status_code(response, 401)
    AssertionProductReviewsError.assert_review_error(response.json(), 401, "Invalid JWT Token")

# TC-579: Admin > Marketing > Product Reviews – Validar error al eliminar review repetidamente
@allure.epic("Módulo de Marketing")
@allure.feature("Product Reviews")
@allure.story("Eliminar reseña de producto")
@allure.title("SYLIUS-579: Validar error al eliminar review repetidamente")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.marketing
@pytest.mark.product_reviews
@pytest.mark.functional_negative
@pytest.mark.functional_edgecase
@pytest.mark.medium
def test_TC579_Eliminar_review_repetidamente(create_product_review):
    headers = create_product_review["headers"]
    review_id = create_product_review["review_id"]
    first_response = ProductReviewsCall.delete(headers, review_id)
    AssertionStatusCode.assert_status_code_204(first_response)
    second_response = ProductReviewsCall.delete(headers, review_id)
    AssertionStatusCode.assert_status_code(second_response, 404)
    AssertionProductReviewsError.assert_review_error(
        second_response.json(), expected_code=404, expected_message="Product review not found" )

# TC-580: Admin > Marketing > Product Reviews – Verificar eliminación concurrente del mismo review desde múltiples solicitudes
@allure.epic("Módulo de Marketing")
@allure.feature("Product Reviews")
@allure.story("Eliminar reseña de producto")
@allure.title("SYLIUS-580: Verificar eliminación concurrente del mismo review desde múltiples solicitudes")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.marketing
@pytest.mark.product_reviews
@pytest.mark.functional_negative
@pytest.mark.functional_edgecase
@pytest.mark.medium
def test_TC580_Eliminar_review_concurrente(create_product_review):
    headers = create_product_review["headers"]
    review_id = create_product_review["review_id"]
    response1 = ProductReviewsCall.delete(headers, review_id)
    response2 = ProductReviewsCall.delete(headers, review_id)
    statuses = sorted([response1.status_code, response2.status_code])
    assert statuses == [204, 404], f"Resultados inesperados: {statuses}"