import pytest
from src.services.request import SyliusRequest
from src.routes.product_reviews_endpoint import ProductReviewsEndpoint
from src.assertions.status_code_assertion import AssertionStatusCode
from src.assertions.product_reviews.schema_assertion import AssertionProductReviews
from src.assertions.product_reviews.error_assertion import AssertionProductReviewsError
from src.assertions.product_reviews.view_content_assertion import AssertionProductReviewsContent


# TC-491: Admin > Marketing > Product Reviews – Obtener lista completa de reseñas de productos
def test_TC491_Obtener_lista_completa_de_reseñas_de_productos(view_product_reviews):
    headers, _, _ = view_product_reviews
    url = ProductReviewsEndpoint.reviews()
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_200(response)
    response_json = response.json()
    AssertionProductReviews.assert_list_schema(response_json)
    AssertionProductReviewsContent.assert_review_collection(response_json)


# TC-492: Admin > Marketing > Product Reviews – Validar error al listar reseñas sin token de autenticación
def test_TC492_Listar_reseñas_sin_token():
    headers = {}
    url = ProductReviewsEndpoint.reviews()
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_401(response)
    AssertionProductReviewsError.assert_review_error(response.json(), 401, "JWT Token not found")


# TC-493: Admin > Marketing > Product Reviews – Validar error al listar reseñas con token inválido
def test_TC493_Listar_reseñas_con_token_invalido():
    headers = {"Authorization": "Bearer invalid_token"}
    url = ProductReviewsEndpoint.reviews()
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_401(response)
    AssertionProductReviewsError.assert_review_error(response.json(), 401, "Invalid JWT Token")


# TC-494: Admin > Marketing > Product Reviews – Obtener lista de reseñas con página igual a 1
# TC-495: Admin > Marketing > Product Reviews – Obtener lista con página mínima válida y cantidad igual a 1
# TC-496: Admin > Marketing > Product Reviews – Obtener lista con página mínima válida y cantidad igual a 0
@pytest.mark.parametrize("page, itemsPerPage", [
    (1, None),
    (1, 1),
    (1, 0)
])
def test_TC_Obtener_lista_de_reseñas_con_paginacion_valida(view_product_reviews, page, itemsPerPage):
    headers, _, _ = view_product_reviews
    params = {"page": page, "itemsPerPage": itemsPerPage}
    params = {k: v for k, v in params.items() if v is not None}
    url = ProductReviewsEndpoint.reviews_with_params(**params)
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_200(response)
    AssertionProductReviewsContent.assert_review_collection(response.json(), params=params)

# TC-497: Admin > Marketing > Product Reviews – Validar error al usar página igual a 0 y cantidad válida 
# TC-498: Admin > Marketing > Product Reviews – Validar error al usar página negativa igual a -1 y cantidad válida 
# TC-499: Admin > Marketing > Product Reviews – Validar error al usar página decimal igual a 1.5 y cantidad válida 
# TC-500: Admin > Marketing > Product Reviews – Validar error al usar página string igual a “uno” y cantidad válida 
# TC-501: Admin > Marketing > Product Reviews – Validar error al usar página vacía y cantidad válida 
# TC-502: Admin > Marketing > Product Reviews – Validar error al usar cantidad mínima válida y página negativa igual a -1 
# TC-503: Admin > Marketing > Product Reviews – Validar error al usar cantidad mínima válida y página decimal igual a 1.5 
# TC-504: Admin > Marketing > Product Reviews – Validar error al usar cantidad mínima válida y página string igual a “uno” 
# TC-505: Admin > Marketing > Product Reviews – Validar error al usar cantidad mínima válida y página vacía
@pytest.mark.parametrize("page, itemsPerPage", [
    (0, 1),
    (-1, 1),
    pytest.param(1.5, 1, marks=pytest.mark.xfail(reason="BUGXX: page decimal rompe la URL")),
    ("uno", 1),
    (" ", 1),
    (1, -1),
    pytest.param(1, 1.5, marks=pytest.mark.xfail(reason="BUGXX: itemsPerPage decimal rompe la URL")),
    pytest.param(1, "uno", marks=pytest.mark.xfail(reason="BUGXX: itemsPerPage string rompe la URL")),
    pytest.param(1, None, marks=pytest.mark.xfail(reason="BUGXX: itemsPerPage vacío rompe la URL"))
])
def test_TC_Obtener_lista_de_reseñas_con_paginacion_invalida(view_product_reviews, page, itemsPerPage):
    headers, _, _ = view_product_reviews
    params = {"page": page, "itemsPerPage": itemsPerPage}
    params = {k: v for k, v in params.items() if v is not None}
    url = ProductReviewsEndpoint.reviews_with_params(**params)
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_400(response)