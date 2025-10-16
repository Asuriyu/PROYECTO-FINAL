import pytest
from src.data.taxons import generate_taxons_data
from src.resources.payloads.taxons_payload import TaxonsPayload
from src.services.call_request.taxons_call import TaxonsCall

@pytest.fixture(scope="module")
def view_taxon(auth_headers):
    payload_taxon1 = TaxonsPayload.build_payload_taxon(generate_taxons_data())
    payload_taxon2 = TaxonsPayload.build_payload_taxon(generate_taxons_data())
    taxon1 = TaxonsCall.create(auth_headers, payload_taxon1)
    taxon2 = TaxonsCall.create(auth_headers, payload_taxon2)
    
    yield auth_headers, taxon1, taxon2

    TaxonsCall.delete(auth_headers, taxon1["code"])
    TaxonsCall.delete(auth_headers, taxon2["code"])