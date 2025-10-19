class AssertionProductReviewsError:

    @staticmethod
    def assert_review_error(response_json, expected_code, expected_message):
        if "status" in response_json and "detail" in response_json:
            assert response_json["status"] == expected_code
            assert response_json["detail"] in [expected_message, "Not Found"]
        elif "code" in response_json and "message" in response_json:
            assert response_json["code"] == expected_code
            assert response_json["message"] in [expected_message, "Not Found"]
        else:
            raise AssertionError(f"Formato de error inesperado: {response_json}")
