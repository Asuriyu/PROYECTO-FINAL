class PromotionsPayload:

    @staticmethod
    def build_payload_promotion(data: dict):
        payload = {
            "code": data.get("code"),
            "name": data.get("name"),
            "description": data.get("description"),
            "priority": data.get("priority"),
            "exclusive": data.get("exclusive"),
            "usageLimit": data.get("usageLimit"),
            "startsAt": data.get("startsAt"),
            "endsAt": data.get("endsAt"),
            "couponBased": data.get("couponBased"),
            "appliesToDiscounted": data.get("appliesToDiscounted"),
            "channels": data.get("channels"),
        }
        return payload

    @staticmethod
    def build_invalid_payload():
        return {
            "code": "",
            "name": None,
            "priority": "invalid",
            "channels": []
        }
    
def build_promotion_payload():
    return {
        "code": "PROMO_E2E",
        "name": "Promoción E2E",
        "description": "Descuento automatizado",
        "priority": 1,
        "exclusive": False,
        "usageLimit": 5,
        "startsAt": "2025-10-18T00:00:00",
        "endsAt": "2025-12-31T00:00:00",
        "couponBased": False,
        "appliesToDiscounted": True,
        "channels": ["/api/v2/admin/channels/FASHION_WEB"]
    }


def build_promotion_update_payload():
    return {
        "name": "Promoción actualizada",
        "priority": 2,
        "exclusive": True
    }