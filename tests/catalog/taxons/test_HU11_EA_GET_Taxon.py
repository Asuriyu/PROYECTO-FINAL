from src.services.request import SyliusRequest
from src.routes.taxons_endpoint import TaxonsEndpoint
from src.assertions.status_code_assertion import AssertionStatusCode
from src.assertions.taxons.schema_assertion import AssertionTaxons
from src.assertions.taxons.view_content_assertions import AssertionTaxonsContent
from src.assertions.taxons.error_assertion import AssertionTaxonsError


def test_TC111_Obtener_taxon_por_code_existente(view_taxon):
    headers, taxon1, _ = view_taxon
    code = taxon1["code"]
    url = TaxonsEndpoint.taxon_code(code)
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_200(response)
    response_json = response.json()
    AssertionTaxons.assert_code_schema(response_json)
    AssertionTaxonsContent.assert_taxon_item(response_json, expected_code=code)

def test_TC112_Validar_error_al_obtener_taxon_por_code_inexistente(view_taxon):
    headers, _, _ = view_taxon
    code = "inexistente"
    url = TaxonsEndpoint.taxon_code(code)
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_404(response)
    AssertionTaxonsError.assert_taxons_error_request(response.json(), 404, "Not Found")

def test_TC113_Validar_error_al_obtener_taxon_sin_autenticacion(view_taxon):
    headers = {}
    code = "test"
    url = TaxonsEndpoint.taxon_code(code)
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_401(response)
    AssertionTaxonsError.assert_taxons_error(response.json(), 401, "JWT Token not found")

def test_TC114_Validar_error_al_obtener_taxon_con_token_invalido(view_taxon):
    headers = {"Authorization": "Bearer invalid_token"}
    code = "test"
    url = TaxonsEndpoint.taxon_code(code)
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_401(response)
    AssertionTaxonsError.assert_taxons_error(response.json(), 401, "Invalid JWT Token")

def test_TC115_Obtener_taxon_con_imagen_asociado(view_taxon):
    headers, taxon1, _ = view_taxon
    code = taxon1["code"]
    url = TaxonsEndpoint.taxon_code(code)
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_200(response)

def test_TC116_Obtener_taxon_sin_imagen_asociado(view_taxon):
    headers, taxon, _ = view_taxon
    code = taxon["code"]
    url = TaxonsEndpoint.taxon_code(code)
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_200(response)