import io
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

@pytest.fixture
def admin_id(auth_headers):
    """Crea un administrador y devuelve su ID."""
    payload = AdministratorsPayload.build_payload_admin(generate_admin_data())
    admin = AdministratorsCall.create(auth_headers, payload)
    yield admin["id"]
    AdministratorsCall.delete(auth_headers, admin["id"])


@pytest.fixture
def disabled_admin_id(auth_headers):
    """Crea un administrador, lo deshabilita y devuelve su ID."""
    payload = AdministratorsPayload.build_payload_admin(generate_admin_data())
    admin = AdministratorsCall.create(auth_headers, payload)
    AdministratorsCall.disable(auth_headers, admin["id"])
    yield admin["id"]
    AdministratorsCall.delete(auth_headers, admin["id"])


@pytest.fixture
def sample_avatar_file():
    return {"file": ("avatar.png", io.BytesIO(b"fake_png_bytes"), "image/png")}


@pytest.fixture
def large_image_file():
    return io.BytesIO(b"x" * (6 * 1024 * 1024))


@pytest.fixture
def tiny_image_file():
    return io.BytesIO(b"x" * 10)