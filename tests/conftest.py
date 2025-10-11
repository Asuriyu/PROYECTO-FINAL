import pytest
from src.config.auth_token import get_token

@pytest.fixture(scope="session")
def auth_headers():
    token = get_token()
    return { 'Authorization': f'Bearer {token}' }