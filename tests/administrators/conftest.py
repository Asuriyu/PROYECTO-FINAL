import pytest
from src.data.administrators import generate_admin_data
from src.resources.payloads.administrators_payload import AdministratorsPayload
from src.services.call_request.administrators_call import AdministratorsCall


@pytest.fixture(scope="module")
def view_admin(auth_headers):
    payload_admin1 = AdministratorsPayload.build_payload_admin(generate_admin_data())
    payload_admin2 = AdministratorsPayload.build_payload_admin(generate_admin_data())
    admin1 = AdministratorsCall.create(auth_headers, payload_admin1)
    admin2 = AdministratorsCall.create(auth_headers, payload_admin2)

    yield auth_headers, admin1, admin2

    AdministratorsCall.delete(auth_headers, admin1["id"])
    AdministratorsCall.delete(auth_headers, admin2["id"])

@pytest.fixture
def admin_data():
    """Devuelve datos de administrador válidos."""
    return generate_admin_data()
