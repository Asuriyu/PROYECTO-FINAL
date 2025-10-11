from src.assertions.schemas_assertions import AssertionSchemas

class AssertionTaxons:
     
    MODULE = "taxons"

    @staticmethod
    def assert_list_schema(response):
          return AssertionSchemas().validate_json_schema(response, "taxons_list_schema.json", AssertionTaxons.MODULE)
    
    @staticmethod
    def assert_code_schema(response):
         return AssertionSchemas().validate_json_schema(response, "taxon_code_schema.json", AssertionTaxons.MODULE)