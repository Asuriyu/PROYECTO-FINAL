import pytest

class AssertionTaxonsError:

    @staticmethod
    def assert_taxons_error(response_json, code, message):
        try:
            assert "code" in response_json, '"code" no está en la respuesta'
            assert "message" in response_json, '"message" no está en la respuesta'
            assert response_json["code"] == code, "Codigo de error no coincide"
            assert response_json["message"] == message, "Mensaje de error no coincide"
        except AssertionError as e:
            pytest.fail(f"[TaxonsError Errors] {e}")

    @staticmethod
    def assert_taxons_error_request(response_json, status, detail):
        try:
            assert "status" in response_json, "'status' no está en la respuesta"
            assert "detail" in response_json, "'detail' no está en la respuesta"
            assert response_json["status"] == status, "Error status no coincide"
            assert response_json["detail"] == detail, "Error detail no coincide"
        except AssertionError as e:
            pytest.fail(f"[TaxonsError Errors Request] {e}")