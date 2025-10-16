# src/assertions/taxons_content_assertions.py
import pytest

TAXON_PREFIX = "/api/v2/admin/taxons/"
TRANS_PREFIX = "/api/v2/admin/taxon/"

class AssertionTaxonsContent:

    @staticmethod
    def assert_taxons_collection(response_json, params=None):
        try:
            members = response_json.get("hydra:member", [])
            assert isinstance(members, list), "'hydra:member' no es lista"
            codes = [it["code"] for it in members]
            assert len(codes) == len(set(codes)), "Hay códigos duplicados en taxons"

            for it in members:
                AssertionTaxonsContent.assert_taxon_item(it)
            if params:
                AssertionTaxonsContent._assert_pagination(response_json, params)

        except AssertionError as e:
            pytest.fail(f"[TaxonsCollection] {e}")

    @staticmethod
    def assert_taxon_item(item, expected_code=None):
        try:
            assert item["@id"].startswith(TAXON_PREFIX), f"@id inesperado: {item['@id']}"
            assert item["@type"] == "Taxon", f"@type inesperado: {item['@type']}"

            assert item["id"] > 0, "id debe ser > 0"
            assert item["position"] >= 0, "position no debe ser negativa"
            assert isinstance(item["enabled"], bool), "enabled no es boolean"

            if expected_code is not None:
                assert item["code"] == expected_code, (
                    f"Código esperado '{expected_code}', encontrado '{item['code']}'"
                )

            # children deben ser URIs del mismo recurso (prefijo)
            for ch in item.get("children", []):
                assert ch.startswith(TAXON_PREFIX), f"children URI inesperada: {ch}"

            # translations: el schema ya valida claves, tipos y campos mínimos.
            translations = item.get("translations", {})
            assert isinstance(translations, dict), "translations no es objeto"
            assert len(translations) >= 1, "Se espera al menos 1 locale en translations"

            # Opcional: validar prefijos de @id dentro de las traducciones
            for _, tr in translations.items():
                assert tr["@id"].startswith(TRANS_PREFIX), f"translations.@id inesperado: {tr['@id']}"
                assert tr["@type"] == "TaxonTranslation", f"translations.@type inesperado: {tr['@type']}"
                assert tr["id"] > 0, "id debe ser > 0"

        except AssertionError as e:
            pytest.fail(f"[TaxonItem] {e}")

    @staticmethod
    def _assert_pagination(response_json, params):
        try:
            items  = params.get("itemsPerPage")
            page = params.get("page", 1)
            if items is None:
                return

            if "hydra:member" in response_json and items == 0:
                assert len(response_json["hydra:member"]) == 0, \
                    "itemsPerPage=0 debería devolver 0 items"

            expected_base = "/api/v2/admin/taxons?itemsPerPage=" + str(items)
            if items != 0:
                expected_base += f"&page={page}"

            view = response_json.get("hydra:view", {})
            assert "@id" in view, "hydra:view.@id ausente"
            assert view["@id"].startswith(expected_base), \
                f"hydra:view.@id no coincide: {view.get('@id')}"

        except AssertionError as e:
            pytest.fail(f"[TaxonsPagination] {e}")