import random
import string

class ProductReviewsPayload:

    @staticmethod
    def generate_unique_string(length=6):
        letters = string.ascii_lowercase + string.digits
        return ''.join(random.choice(letters) for _ in range(length))

    @staticmethod
    def build_payload_product_review(data):
        title = data.get("title", f"Reseña_{ProductReviewsPayload.generate_unique_string()}")
        rating = data.get("rating", random.randint(1, 5))
        comment = data.get("comment", "Comentario generado automáticamente para pruebas.")
        author = data.get("author", f"tester_{ProductReviewsPayload.generate_unique_string()}")
        product = data.get("product", "/api/v2/shop/products/TEST_PRODUCT")

        payload_review = {
            "title": title,
            "rating": rating,
            "comment": comment,
            "author": author,
            "product": product,
            "status": data.get("status", "new"),
            "createdAt": data.get("createdAt", None),
        }

        return payload_review