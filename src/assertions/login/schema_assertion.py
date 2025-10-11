from src.assertions.schemas_assertions import AssertionSchemas

class AssertionLogin:
     
    MODULE = "login"

    @staticmethod
    def assert_input_schema(response):
          return AssertionSchemas().validate_json_schema(response, "input_schema.json", AssertionLogin.MODULE)
    
    @staticmethod
    def assert_output_schema(response):
         return AssertionSchemas().validate_json_schema(response, "output_schema.json", AssertionLogin.MODULE)