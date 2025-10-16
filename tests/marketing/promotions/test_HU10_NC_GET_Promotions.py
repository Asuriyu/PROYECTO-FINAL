import pytest
from src.services.request import SyliusRequest
from src.routes.promotions_endpoint import PromotionsEndpoint
from src.assertions.status_code_assertion import AssertionStatusCode
from src.assertions.promotions.schema_assertion import AssertionPromotions
from src.assertions.promotions.error_assertion import AssertionPromotionsError
from src.assertions.promotions.view_content_assertion import AssertionPromotionsContent

# TC-461: Admin > Marketing > Promotions – Obtener lista completa de promociones
def test_TC461_Obtener_lista_completa_de_promociones(view_promotions):
    headers, _, _ = view_promotions
    url = PromotionsEndpoint.promotions()
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_200(response)
    response_json = response.json()
    AssertionPromotions.assert_list_schema(response_json)
    AssertionPromotionsContent.assert_promotion_collection(response_json)

# TC-462: Admin > Marketing > Promotions – Validar error al listar promociones sin token de autenticación
def test_TC462_Listar_promociones_sin_token():
    headers = {}
    url = PromotionsEndpoint.promotions()
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_401(response)
    AssertionPromotionsError.assert_promotion_error(response.json(), 401, "JWT Token not found")

# TC-463: Admin > Marketing > Promotions – Validar error al listar promociones con token inválido
def test_TC463_Listar_promociones_con_token_invalido():
    headers = {"Authorization": "Bearer invalid_token"}
    url = PromotionsEndpoint.promotions()
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_401(response)
    AssertionPromotionsError.assert_promotion_error(response.json(), 401, "Invalid JWT Token")

# TC-464: Admin > Marketing > Promotions – Obtener lista de promociones con página igual a 1
# TC-465: Admin > Marketing > Promotions – Obtener lista con página mínima válida y cantidad igual a 1
# TC-466: Admin > Marketing > Promotions – Obtener lista con página mínima válida y cantidad igual a 0
@pytest.mark.parametrize("page, itemsPerPage", [
    (1, None),
    (1, 1),
    (1, 0)
])
def test_TC_Obtener_lista_de_promociones_con_paginacion_valida(view_promotions, page, itemsPerPage):
    headers, _, _ = view_promotions
    params = {"page": page, "itemsPerPage": itemsPerPage}
    params = {k: v for k, v in params.items() if v is not None}
    url = PromotionsEndpoint.promotions_with_params(**params)
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_200(response)
    AssertionPromotionsContent.assert_promotion_collection(response.json(), params=params)

# TC-467: Admin > Marketing > Promotions – Validar error al usar página igual a 0 y cantidad válida
# TC-468: Admin > Marketing > Promotions – Validar error al usar página negativa igual a -1 y cantidad válida
# TC-469: Admin > Marketing > Promotions – Validar error al usar página decimal igual a 1.5 y cantidad válida
# TC-470: Admin > Marketing > Promotions – Validar error al usar página string igual a “uno” y cantidad válida
# TC-471: Admin > Marketing > Promotions – Validar error al usar página vacía y cantidad válida
# TC-472: Admin > Marketing > Promotions – Validar error al usar página mínima válida y cantidad negativa igual a -1
# TC-473: Admin > Marketing > Promotions – Validar error al usar página mínima válida y cantidad decimal igual a 1.5
# TC-474: Admin > Marketing > Promotions – Validar error al usar página mínima válida y cantidad string igual a “uno”
# TC-475: Admin > Marketing > Promotions – Validar error al usar página mínima válida y cantidad vacía
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
def test_TC_Obtener_lista_de_promociones_con_paginacion_invalida(view_promotions, page, itemsPerPage):
    headers, _, _ = view_promotions
    params = {"page": page, "itemsPerPage": itemsPerPage}
    params = {k: v for k, v in params.items() if v is not None}
    url = PromotionsEndpoint.promotions_with_params(**params)
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_400(response)