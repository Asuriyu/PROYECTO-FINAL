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
    response = ProductReviewsCall.get_all(auth_headers)
    AssertionStatusCode.assert_status_code_200(response)
    response_json = response.json()

    if "hydra:member" not in response_json or not response_json["hydra:member"]:
        pytest.skip("No hay reviews disponibles en el sistema para eliminar.")

    first_review = response_json["hydra:member"][0]
    review_id = first_review["@id"].split("/")[-1]

    yield {
        "headers": auth_headers,
        "review_id": review_id
    }