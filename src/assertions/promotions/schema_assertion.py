from src.assertions.schemas_assertions import AssertionSchemas

class AssertionPromotions:

    MODULE = "promotions"

    @staticmethod
    def assert_create_schema(response):
        return AssertionSchemas().validate_json_schema(
            response, "promotion_create_schema.json", AssertionPromotions.MODULE
        )

    @staticmethod
    def assert_list_schema(response):
        return AssertionSchemas().validate_json_schema(
            response, "promotions_list_schema.json", AssertionPromotions.MODULE
        )

    @staticmethod
    def assert_get_schema(response):
        return AssertionSchemas().validate_json_schema(
            response, "promotion_get_schema.json", AssertionPromotions.MODULE
        )

    @staticmethod
    def assert_update_schema(response):
        return AssertionSchemas().validate_json_schema(
            response, "promotion_update_schema.json", AssertionPromotions.MODULE
        )

    @staticmethod
    def assert_archive_schema(response):
        return AssertionSchemas().validate_json_schema(
            response, "promotion_archive_schema.json", AssertionPromotions.MODULE
        )

    @staticmethod
    def assert_restore_schema(response):
        return AssertionSchemas().validate_json_schema(
            response, "promotion_restore_schema.json", AssertionPromotions.MODULE
        )

    @staticmethod
    def assert_delete_schema(response):
        return AssertionSchemas().validate_json_schema(
            response, "promotion_delete_schema.json", AssertionPromotions.MODULE
        )