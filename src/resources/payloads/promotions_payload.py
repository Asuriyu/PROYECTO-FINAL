class PromotionsPayload:

    @staticmethod
    def build_payload_promotion(data: dict):
        """
        Construye el payload JSON que se enviará en POST o PUT.
        """
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
        """Payload inválido para pruebas negativas."""
        return {
            "code": "",
            "name": None,
            "priority": "invalid",
            "channels": []
        }