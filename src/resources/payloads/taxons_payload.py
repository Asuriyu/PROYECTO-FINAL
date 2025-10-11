class TaxonsPayload:

    @staticmethod
    def build_payload_taxon(data):
        
        payload_taxon = {
            "code": data["code"],
            "translations": {
                "en_US": {
                    "name": data["translations"]["en_US"]["name"],
                    "slug": data["translations"]["en_US"]["slug"],
                    "description": data["translations"]["en_US"]["description"]
                }
            },
            "parent": data["parent"],
            "enabled": data["enabled"]
        }

        return payload_taxon