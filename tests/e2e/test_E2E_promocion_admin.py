import pytest
import requests
import allure
import os
from src.routes.endpoint import LOGIN2, PROMOTIONS
from src.resources.payloads.promotions_payload import (
    build_promotion_payload,
    build_promotion_update_payload
)
from src.utils.logger_helpers import setup_logger, log_request_response

@pytest.mark.e2e
@allure.epic("E2E - Marketing")
@allure.feature("Promotions")
@allure.story("HU07 - Flujo completo de gestión de promociones (Admin)")
def test_e2e_promocion_admin():
    setup_logger()
    logging = __import__("logging")
    logging.info("INICIO TEST E2E PROMOCIÓN ADMIN")

    with allure.step("Autenticar al administrador"):
        credentials = {
            "email": os.getenv("ADMIN_EMAIL"),
            "password": os.getenv("ADMIN_PASSWORD"),
        }
        resp_login = requests.post(LOGIN2, json=credentials)
        log_request_response("POST", LOGIN2, resp_login, payload=credentials)
        assert resp_login.status_code == 200, f"Error login: {resp_login.text}"
        token = resp_login.json().get("token")
        assert token, "No se obtuvo token"
        headers = {"Authorization": f"Bearer {token}"}

    with allure.step("Crear promoción nueva"):
        promo_payload = build_promotion_payload()
        create = requests.post(PROMOTIONS, json=promo_payload, headers=headers)
        log_request_response("POST", PROMOTIONS, create, headers=headers, payload=promo_payload)
        assert create.status_code == 201, f"Error creando promoción: {create.text}"
        code = promo_payload["code"]

    with allure.step("Consultar promoción creada"):
        get = requests.get(f"{PROMOTIONS}/{code}", headers=headers)
        log_request_response("GET", f"{PROMOTIONS}/{code}", get, headers=headers)
        assert get.status_code == 200, f"No se encontró promoción: {get.text}"
        allure.attach(str(get.json()), "Datos promoción", allure.attachment_type.JSON)

    with allure.step("Actualizar promoción"):
        update_payload = build_promotion_update_payload()
        put = requests.put(f"{PROMOTIONS}/{code}", json=update_payload, headers=headers)
        log_request_response("PUT", f"{PROMOTIONS}/{code}", put, headers=headers, payload=update_payload)
        assert put.status_code in [200, 204], f"Error actualizando: {put.text}"

    with allure.step("Archivar y restaurar promoción"):
        archive = requests.patch(f"{PROMOTIONS}/{code}/archive", headers=headers)
        log_request_response("PATCH", f"{PROMOTIONS}/{code}/archive", archive, headers=headers)
        assert archive.status_code in [200, 204], f"No se pudo archivar: {archive.text}"
        restore = requests.patch(f"{PROMOTIONS}/{code}/restore", headers=headers)
        log_request_response("PATCH", f"{PROMOTIONS}/{code}/restore", restore, headers=headers)
        assert restore.status_code in [200, 204], f"No se pudo restaurar: {restore.text}"

    with allure.step("Eliminar promoción"):
        delete = requests.delete(f"{PROMOTIONS}/{code}", headers=headers)
        log_request_response("DELETE", f"{PROMOTIONS}/{code}", delete, headers=headers)
        assert delete.status_code in [200, 204], f"No se eliminó: {delete.text}"

    with allure.step("Confirmar eliminación"):
        confirm = requests.get(f"{PROMOTIONS}/{code}", headers=headers)
        log_request_response("GET", f"{PROMOTIONS}/{code}", confirm, headers=headers)
        assert confirm.status_code == 404, f"La promoción aún existe: {confirm.text}"

    logging.info("FIN TEST E2E PROMOCIÓN ADMIN ")
