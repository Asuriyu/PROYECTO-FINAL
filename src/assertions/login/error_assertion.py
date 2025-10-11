import pytest
class AssertionLoginError:
    @staticmethod
    def assert_login_error(response_json, code, message):
        try:
            assert "code" in response_json, "'code' no está en la respuesta"
            assert "message" in response_json, "'message' no está en la respuesta"
            assert response_json["code"] == code, "Error code no coincide"
            assert response_json["message"] == message, "Error message no coincide"
        except AssertionError as e:
            pytest.fail(f"Mensajes de error erroneos: {e}")