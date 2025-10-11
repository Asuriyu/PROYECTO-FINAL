from src.assertions.schemas_assertions import AssertionSchemas

class AssertionAdministrators:
    
    MODULE = "administrators"

    @staticmethod
    def assert_create_schema(response):
        return AssertionSchemas().validate_json_schema(
            response, "admin_code_schema.json", AssertionAdministrators.MODULE
        )

    @staticmethod
    def assert_list_schema(response):
        return AssertionSchemas().validate_json_schema(
            response, "admins_lista_schema.json", AssertionAdministrators.MODULE
        )