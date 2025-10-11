import random
import string

class AdministratorsPayload:

    @staticmethod
    def generate_unique_string(length=6):
        letters = string.ascii_lowercase + string.digits
        return ''.join(random.choice(letters) for _ in range(length))

    @staticmethod
    def build_payload_admin(data):
        username = data.get("username")
        if not username:
            username = f"user_{AdministratorsPayload.generate_unique_string()}"

        email = data.get("email")
        if not email:
            email = f"{AdministratorsPayload.generate_unique_string()}@example.com"
        payload_admin = {
            "firstName": data.get("firstName", "TestFirstName"),
            "lastName": data.get("lastName", "TestLastName"),
            "username": username,
            "plainPassword": data.get("plainPassword", "123456"),
            "email": email,
            "enabled": data.get("enabled", True),          
            "localeCode": data.get("localeCode", "es_ES") 
        }

        return payload_admin