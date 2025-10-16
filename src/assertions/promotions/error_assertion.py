import pytest

class AssertionPromotionsError:

    @staticmethod
    def assert_promotion_error(response_json, code, message):
        try:
            if "@type" in response_json and response_json["@type"] == "hydra:Error":
                expected_status = response_json.get("status") or response_json.get("code")
                assert expected_status == code, f"Código esperado {code}, recibido {expected_status}"
                assert "detail" in response_json, "'detail' no está en la respuesta"
                detail = response_json["detail"].lower()
                message_ok = message.lower() in detail or "not found" in detail
                assert message_ok, (
                    f"Mensaje esperado '{message}', recibido '{response_json['detail']}'"
                )
                return
            
            assert "code" in response_json, '"code" no está en la respuesta'
            assert "message" in response_json, '"message" no está en la respuesta'
            assert response_json["code"] == code, "Código de error no coincide"
            assert response_json["message"] == message, "Mensaje de error no coincide"
        except AssertionError as e:
            pytest.fail(f"[PromotionsError] {e}")

    @staticmethod
    def assert_promotion_error_request(response_json, status, detail):
        try:
            assert "status" in response_json, "'status' no está en la respuesta"
            assert "detail" in response_json, "'detail' no está en la respuesta"
            assert response_json["status"] == status, "Error status no coincide"
            assert response_json["detail"] == detail, "Error detail no coincide"
        except AssertionError as e:
            pytest.fail(f"[PromotionsErrorRequest] {e}")

    @staticmethod
    def assert_authentication_error(response_json):
        assert "message" in response_json or "detail" in response_json, "Falta 'message' o 'detail'"
        message = (response_json.get("message") or response_json.get("detail")).lower()
        expected_phrases = [
            "unauthorized",
            "invalid token",
            "authentication required",
            "jwt token not found",
            "invalid jwt token",
        ]
        assert any(p in message for p in expected_phrases), \
            f"Mensaje inesperado: {response_json}"

    @staticmethod
    def assert_not_found_error(response_json):
        assert isinstance(response_json, dict), "La respuesta no es un diccionario válido"
        msg = response_json.get("message") or response_json.get("detail")
        assert msg is not None, f"No se encontró 'message' ni 'detail' en la respuesta: {response_json}"
        msg_lower = msg.lower()
        assert (
            "not found" in msg_lower
            or "no existe" in msg_lower
            or "promotion" in msg_lower
        ), f"Mensaje inesperado: {msg}"

    @staticmethod
    def assert_already_archived_error(response_json):
        msg = response_json.get("message") or response_json.get("detail")
        assert msg, "No se encontró 'message' ni 'detail' en la respuesta"
        msg_lower = msg.lower()
        assert (
            "already archived" in msg_lower
            or "ya archivada" in msg_lower
            or "promotion archived" in msg_lower
        ), f"Mensaje inesperado: {msg}"

    @staticmethod
    def assert_not_archived_error(response_json):
        msg = response_json.get("message") or response_json.get("detail")
        assert msg, "No se encontró 'message' ni 'detail' en la respuesta"
        msg_lower = msg.lower()
        assert (
            "not archived" in msg_lower
            or "no archivada" in msg_lower
            or "promotion not archived" in msg_lower
        ), f"Mensaje inesperado: {msg}"

    @staticmethod
    def assert_missing_field_error(response_json):
        msg = response_json.get("message") or response_json.get("detail")
        assert msg, "No se encontró 'message' ni 'detail' en la respuesta"
        msg_lower = msg.lower()
        assert (
            "missing" in msg_lower
            or "required" in msg_lower
            or "falta" in msg_lower
        ), f"Mensaje inesperado: {msg}"

    @staticmethod
    def assert_duplicate_code_error(response_json):
        msg = response_json.get("message") or response_json.get("detail")
        assert msg, "No se encontró 'message' ni 'detail' en la respuesta"
        msg_lower = msg.lower()
        assert (
            "already exists" in msg_lower
            or "duplicado" in msg_lower
            or "code" in msg_lower
        ), f"Mensaje inesperado: {msg}"