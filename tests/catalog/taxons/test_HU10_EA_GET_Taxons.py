import pytest

from src.services.request import SyliusRequest
from src.routes.taxons_endpoint import TaxonsEndpoint
from src.assertions.status_code_assertion import AssertionStatusCode
from src.assertions.taxons.schema_assertion import AssertionTaxons
from src.assertions.taxons.view_content_assertions import AssertionTaxonsContent
from src.assertions.taxons.error_assertion import AssertionTaxonsError

# TC-106: Catalog > Taxons - Obtener lista de taxones
def test_TC106_Obtener_lista_de_taxones(view_taxon):
    headers, _, _ = view_taxon
    url = TaxonsEndpoint.taxon()
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_200(response)
    response_json = response.json()
    AssertionTaxons.assert_list_schema(response_json)
    AssertionTaxonsContent.assert_taxons_collection(response_json)

# TC-107: Catalog > Taxons - Validar error al listar taxones sin token de autenticación
def test_TC107_Listar_taxones_sin_autenticacion():
    headers = {}
    url = TaxonsEndpoint.taxon()
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_401(response)
    AssertionTaxonsError.assert_taxons_error(response.json(), 401, "JWT Token not found")

# TC-108: Catalog > Taxons - Validar error al listar taxones con token inválido
def test_TC108_Listar_taxones_con_token_invalido():
    headers = {"Authorization": "Bearer invalid_token"}
    url = TaxonsEndpoint.taxon()
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_401(response)
    AssertionTaxonsError.assert_taxons_error(response.json(), 401, "Invalid JWT Token")

# TC-109: Catalog > Taxons - Obtener lista de taxones con página igual a 1
# TC-110: Catalog > Taxons - Obtener lista de taxones con página mínima válida y cantidad igual 1
# TC-357: Catalog > Taxons - Obtener lista de taxones con página mínima válida y cantidad igual a 0
@pytest.mark.parametrize("page, itemsPerPage", [
    (1, None),
    (1, 1),
    (1, 0)
])
def test_TC_Obtener_lista_de_taxones_con_paginacion_valida(view_taxon, page, itemsPerPage):
    headers, _, _ = view_taxon
    params = {"page": page, "itemsPerPage": itemsPerPage}
    params = {k: v for k, v in params.items() if v is not None}
    url = TaxonsEndpoint.taxons_with_params(**params)
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_200(response)
    AssertionTaxonsContent.assert_taxons_collection(response.json(), params=params)

# TC-358: Catalog > Taxons - Validar error al usar página igual a 0 y cantidad válida
# TC-359: Catalog > Taxons - Validar error al usar página negativa igual a -1 y cantidad válida
# TC-360: Catalog > Taxons - Validar error al usar página decimal igual a 1.5 y cantidad válida
# TC-361: Catalog > Taxons - Validar error al usar página string igual a “uno” y cantidad válida
# TC-362: Catalog > Taxons - Validar error al usar página vacía y cantidad válida
# TC-363: Catalog > Taxons - Validar error al usar página mínima válida y cantidad negativa igual a -1
# TC-364: Catalog > Taxons - Validar error al usar página mínima válida y cantidad decimal igual a 1.5
# TC-365: Catalog > Taxons - Validar error al usar página mínima válida y cantidad string igual a “uno”
# TC-366: Catalog > Taxons - Validar error al usar página mínima válida y cantidad vacía
@pytest.mark.parametrize("page, itemsPerPage", [
    (0, 1),
    (-1, 1),
    pytest.param(1.5, 1, marks=pytest.mark.xfail(reason="BUGXX: Al listar inventarios con parámetro page acepta decimales y rompe la URL", run=True)),
    ("uno", 1),
    (" ", 1), #Revisar en Action, porque linux no reconoce espacios.
    (1, -1),
    pytest.param(1, 1.5, marks=pytest.mark.xfail(reason="BUGXX: Al listar inventarios con parámetro itemsPerPage puede ser decimal rompiendo la URL", run=True)),
    pytest.param(1, "uno", marks=pytest.mark.xfail(reason="BUGXX: Al listar inventarios con parámetro itemsPerPage puede ser string rompiendo la URL", run=True)),
    pytest.param(1, None, marks=pytest.mark.xfail(reason="BUGXX: Al listar inventarios con parámetro itemsPerPage puede ser vacío rompiendo la URL", run=True))
])
def test_TC_Obtener_lista_de_taxones_con_paginacion_invalida(view_taxon, page, itemsPerPage):
    headers, _, _ = view_taxon
    params = {"page": page, "itemsPerPage": itemsPerPage}
    params = {k: v for k, v in params.items() if v is not None}
    url = TaxonsEndpoint.taxons_with_params(**params)
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_400(response)