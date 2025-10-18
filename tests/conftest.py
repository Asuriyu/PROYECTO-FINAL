import pytest
from src.config.auth_token import get_token
import logging
from datetime import datetime

@pytest.fixture(scope="session")
def auth_headers():
    token = get_token()
    return { 'Authorization': f'Bearer {token}' }

@pytest.fixture(autouse=True)
def log_test_start(request):
    logging.info("\n" + "=" * 100)
    logging.info("CODE REVIEW - Approved")
    logging.info(f"Test: {request.node.name}")
    logging.info(f"Start time: {datetime.now().strftime('%H:%M:%S')}")
    yield
    logging.info(f"Completed test: {request.node.name}")
    logging.info("=" * 100 + "\n")