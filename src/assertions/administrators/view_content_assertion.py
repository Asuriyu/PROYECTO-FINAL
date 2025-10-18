import pytest

ADMIN_PREFIX = "/api/v2/admin/administrators/"

class AssertionAdministratorsContent:

    @staticmethod
    def assert_admin_item(item, expected_username=None):
        try:
            assert item["@id"].startswith(ADMIN_PREFIX), f"@id inesperado: {item['@id']}"
            assert item["@type"] == "Administrator", f"@type inesperado: {item['@type']}"
            
            assert item["id"] > 0, "id debe ser > 0"
            assert isinstance(item["enabled"], bool), "enabled no es boolean"
            assert isinstance(item["firstName"], (str, type(None))), "firstName debe ser string o null"
            assert isinstance(item["lastName"], (str, type(None))), "lastName debe ser string o null"
            assert isinstance(item["username"], str), "username debe ser string"
            assert isinstance(item["email"], str), "email debe ser string"

            if expected_username is not None:
                assert item["username"] == expected_username, (
                    f"Username esperado '{expected_username}', encontrado '{item['username']}'"
                )

        except AssertionError as e:
            pytest.fail(f"[AdministratorItem] {e}")

    @staticmethod
    def assert_admin_enabled_state(item, expected_state):
        try:
            assert isinstance(item["enabled"], bool), "enabled no es boolean"
            assert item["enabled"] == expected_state, f"Estado enabled esperado {expected_state}, encontrado {item['enabled']}"
        except AssertionError as e:
            pytest.fail(f"[AdministratorEnabledState] {e}")

    @staticmethod
    def assert_admin_collection(response_json, params=None):
        try:
            members = response_json.get("hydra:member", [])
            assert isinstance(members, list), "'hydra:member' no es lista"
            usernames = [it["username"] for it in members]
            assert len(usernames) == len(set(usernames)), "Hay usernames duplicados en administrators"

            for it in members:
                AssertionAdministratorsContent.assert_admin_item(it)

            if params:
                AssertionAdministratorsContent._assert_pagination(response_json, params)

        except AssertionError as e:
            pytest.fail(f"[AdministratorsCollection] {e}")

    @staticmethod
    def _assert_pagination(response_json, params):
        try:
            items = params.get("itemsPerPage")
            page = params.get("page", 1)
            if items is None:
                return

            if "hydra:member" in response_json and items == 0:
                assert len(response_json["hydra:member"]) == 0, \
                    "itemsPerPage=0 debería devolver 0 items"

            expected_base = "/api/v2/admin/administrators?itemsPerPage=" + str(items)
            if items != 0:
                expected_base += f"&page={page}"

            view = response_json.get("hydra:view", {})
            assert "@id" in view, "hydra:view.@id ausente"
            assert view["@id"].startswith(expected_base), \
                f"hydra:view.@id no coincide: {view.get('@id')}"

        except AssertionError as e:
            pytest.fail(f"[AdministratorsPagination] {e}")