class AssertionProductReviewsContent:

    @staticmethod
    def assert_review_collection(response_json, params=None):
        assert "hydra:member" in response_json, "No existe 'hydra:member' en la respuesta"
        assert isinstance(response_json["hydra:member"], list), "'hydra:member' debe ser una lista"

        if len(response_json["hydra:member"]) > 0:
            first_review = response_json["hydra:member"][0]
            assert "id" in first_review, "Falta campo 'id' en reseña"
            assert "rating" in first_review, "Falta campo 'rating' en reseña"
            assert "status" in first_review, "Falta campo 'status' en reseña"
        if params:
            for key, value in params.items():
                assert key in ["page", "itemsPerPage"], f"Parámetro no reconocido: {key}"

        assert "@type" in response_json, "Falta '@type' en la respuesta"
        assert response_json["@type"] in ["hydra:Collection", "Collection"], \
            f"Tipo inesperado de colección: {response_json.get('@type')}"