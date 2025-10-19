class AssertionProductReviewsError:

    @staticmethod
    def assert_review_error(response_json, expected_code, expected_message):
        assert "code" in response_json, "Falta el campo 'code' en la respuesta"
        assert "message" in response_json, "Falta el campo 'message' en la respuesta"
        assert response_json["code"] == expected_code, \
            f"Código esperado {expected_code}, obtenido {response_json['code']}"
        assert expected_message in response_json["message"], \
            f"Mensaje esperado '{expected_message}', obtenido '{response_json['message']}'"