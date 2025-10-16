from src.assertions.schemas_assertions import AssertionSchemas

class AssertionPromotions:

    MODULE = "promotions"

    @staticmethod
    def assert_create_schema(response):
        """Valida el esquema JSON al crear una promoción"""
        return AssertionSchemas().validate_json_schema(
            response, "promotion_create_schema.json", AssertionPromotions.MODULE
        )

    @staticmethod
    def assert_list_schema(response):
        """Valida el esquema JSON al listar promociones"""
        return AssertionSchemas().validate_json_schema(
            response, "promotions_list_schema.json", AssertionPromotions.MODULE
        )

    @staticmethod
    def assert_get_schema(response):
        """Valida el esquema JSON al consultar una promoción específica"""
        return AssertionSchemas().validate_json_schema(
            response, "promotion_get_schema.json", AssertionPromotions.MODULE
        )

    @staticmethod
    def assert_update_schema(response):
        """Valida el esquema JSON al actualizar una promoción"""
        return AssertionSchemas().validate_json_schema(
            response, "promotion_update_schema.json", AssertionPromotions.MODULE
        )

    @staticmethod
    def assert_archive_schema(response):
        """Valida el esquema JSON al archivar una promoción"""
        return AssertionSchemas().validate_json_schema(
            response, "promotion_archive_schema.json", AssertionPromotions.MODULE
        )

    @staticmethod
    def assert_restore_schema(response):
        """Valida el esquema JSON al restaurar una promoción archivada"""
        return AssertionSchemas().validate_json_schema(
            response, "promotion_restore_schema.json", AssertionPromotions.MODULE
        )

    @staticmethod
    def assert_delete_schema(response):
        """Valida el esquema JSON al eliminar una promoción"""
        return AssertionSchemas().validate_json_schema(
            response, "promotion_delete_schema.json", AssertionPromotions.MODULE
        )