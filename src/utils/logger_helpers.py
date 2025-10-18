import logging
import json
import os

def setup_logger():
    log_dir = os.path.join("reports", "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "tests.log")
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(levelname)s | %(asctime)s | %(message)s",
        datefmt="%H:%M:%S",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_file, mode="a", encoding="utf-8")
        ]
    )

def log_request_response(method, url, response, headers=None, payload=None):
    """
    INFO:  Método, dominio e IP
    DEBUG: URL, Headers, Payload, Response
    """
    logging.info("=" * 100)
    logging.info(f"REQUEST METHOD: {method}")
    logging.info(f"IP ADDRESS OR DOMAIN: {url.split('/')[2]}")
    logging.debug(f"REQUEST URL: {url}")
    logging.info(f"STATUS CODE: {response.status_code}")

    if headers:
        try:
            headers_dict = dict(headers)
        except Exception:
            headers_dict = headers
        logging.debug("REQUEST HEADERS:\n%s", json.dumps(headers_dict, indent=4, ensure_ascii=False))

    if payload:
        logging.debug("PAYLOAD REQUEST:\n%s", json.dumps(payload, indent=4, ensure_ascii=False))

    try:
        if response.content and len(response.content) > 0:
            logging.debug("RESPONSE:\n%s", json.dumps(response.json(), indent=4, ensure_ascii=False))
        else:
            logging.debug("RESPONSE: No content (empty body)")
    except Exception:
        logging.debug("RESPONSE TEXT:\n%s", response.text or "No content")

    logging.info("=" * 100)