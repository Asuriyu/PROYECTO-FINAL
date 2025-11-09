import jsonschema

class AssertionProductReviews:

    @staticmethod
    def assert_list_schema(response_json):
        schema = {
            "type": "object",
            "required": ["@context", "@id", "@type", "hydra:member"],
            "properties": {
                "@context": {"type": "string"},
                "@id": {"type": "string"},
                "@type": {"type": "string"},
                "hydra:member": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "@id": {"type": "string"},
                            "@type": {"type": "string"},
                            "id": {"type": "integer"},
                            "title": {"type": ["string", "null"]},
                            "comment": {"type": ["string", "null"]},
                            "rating": {"type": ["integer", "null"]},
                            "status": {"type": ["string", "null"]},
                            "author": {"type": ["string", "null"]},
                            "product": {"type": ["string", "null"]},
                            "createdAt": {"type": ["string", "null"]},
                            "updatedAt": {"type": ["string", "null"]}
                        },
                        "required": ["@id", "@type", "id"]
                    }
                },
                "hydra:totalItems": {"type": ["integer", "null"]}
            }
        }
        jsonschema.validate(instance=response_json, schema=schema)