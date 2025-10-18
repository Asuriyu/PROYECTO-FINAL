import pytest

PROMOTION_PREFIX = "/api/v2/admin/promotions/"

class AssertionPromotionsContent:

    @staticmethod
    def assert_promotion_item(item, expected_code=None):
        try:
            assert item["@id"].startswith(PROMOTION_PREFIX), f"@id inesperado: {item['@id']}"
            assert item["@type"] == "Promotion", f"@type inesperado: {item['@type']}"
            assert item["id"] > 0, "id debe ser > 0"
            assert isinstance(item["code"], str), "code debe ser string"
            assert isinstance(item["name"], str), "name debe ser string"
            assert isinstance(item["description"], (str, type(None))), "description debe ser string o null"
            assert isinstance(item["priority"], int), "priority debe ser entero"
            assert isinstance(item["exclusive"], bool), "exclusive debe ser boolean"
            assert isinstance(item["appliesToDiscounted"], bool), "appliesToDiscounted debe ser boolean"
            assert isinstance(item["couponBased"], bool), "couponBased debe ser boolean"

            if item.get("startsAt"):
                starts = item["startsAt"]
                assert isinstance(starts, str), "startsAt debe ser string"
                assert any(sep in starts for sep in ["T", " "]), f"Formato inválido en startsAt: {starts}"
                assert starts[:4].isdigit() and starts[4] == "-", f"Formato inesperado en startsAt: {starts}"

            if item.get("endsAt"):
                ends = item["endsAt"]
                assert isinstance(ends, str), "endsAt debe ser string"
                assert any(sep in ends for sep in ["T", " "]), f"Formato inválido en endsAt: {ends}"
                assert ends[:4].isdigit() and ends[4] == "-", f"Formato inesperado en endsAt: {ends}"

            assert isinstance(item["channels"], list), "channels debe ser lista"
            for ch in item["channels"]:
                assert isinstance(ch, str), f"Channel inválido (no es string): {ch}"
                assert (
                    ch.startswith("http") or ch.startswith("/api/")
            ), f"Canal inválido: {ch}"

            if expected_code is not None:
                assert item["code"], "El campo 'code' no debe estar vacío"


        except AssertionError as e:
            pytest.fail(f"[PromotionItem] {e}")

    @staticmethod
    def assert_promotion_priority(item, expected_priority):
        try:
            assert isinstance(item["priority"], int), "priority no es entero"
            assert item["priority"] == expected_priority, (
                f"Priority esperado {expected_priority}, encontrado {item['priority']}"
            )
        except AssertionError as e:
            pytest.fail(f"[PromotionPriority] {e}")

    @staticmethod
    def assert_promotion_collection(response_json, params=None):
        try:
            members = response_json.get("hydra:member", [])
            assert isinstance(members, list), "'hydra:member' no es lista"
            codes = [it["code"] for it in members]
            assert len(codes) == len(set(codes)), "Hay codes duplicados en promotions"
            for it in members:
                AssertionPromotionsContent.assert_promotion_item(it)
            if params:
                AssertionPromotionsContent._assert_pagination(response_json, params)
        except AssertionError as e:
            pytest.fail(f"[PromotionsCollection] {e}")

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
            expected_base = "/api/v2/admin/promotions?itemsPerPage=" + str(items)
            if items != 0:
                expected_base += f"&page={page}"
            view = response_json.get("hydra:view", {})
            assert "@id" in view, "hydra:view.@id ausente"
            assert view["@id"].startswith(expected_base), \
                f"hydra:view.@id no coincide: {view.get('@id')}"
        except AssertionError as e:
            pytest.fail(f"[PromotionsPagination] {e}")