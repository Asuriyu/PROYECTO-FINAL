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