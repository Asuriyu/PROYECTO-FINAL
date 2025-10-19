import pytest
from src.services.call_request.product_reviews_call import ProductReviewsCall
from src.assertions.status_code_assertion import AssertionStatusCode


@pytest.fixture(scope="module")
def view_product_reviews(auth_headers):

    response = ProductReviewsCall.get_all(auth_headers)
    AssertionStatusCode.assert_status_code_200(response)
    response_json = response.json()
    reviews = response_json.get("hydra:member", [])
    yield auth_headers, response_json, reviews

@pytest.fixture
def create_product_review(auth_headers):
    payload = {
        "title": "Excelente producto",
        "rating": 5,
        "comment": "Muy buena calidad y envío rápido.",
        "author": {
            "email": "qa_tester@example.com",
            "firstName": "QA",
            "lastName": "Tester"
        },
        "reviewSubject": "/api/v2/shop/products/TEST_PRODUCT"
    }
    response = ProductReviewsCall.create(auth_headers, payload)
    AssertionStatusCode.assert_status_code_201(response)
    review_data = response.json()
    assert "@id" in review_data, "No se creó correctamente la reseña"
    review_id = review_data.get("@id").split("/")[-1]

    yield {
        "headers": auth_headers,
        "review_id": review_id,
        "payload": payload,
        "response": review_data
    }
    ProductReviewsCall.delete(auth_headers, review_id)