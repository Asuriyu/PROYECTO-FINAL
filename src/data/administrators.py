from faker import Faker
import re

fake = Faker()

def generate_admin_data(required_only=False):
    first_name = fake.first_name()
    last_name = fake.last_name() 
    username_base = f"{first_name[:3]}{last_name[:3]}{fake.random_int(1, 999)}".lower()
    username = re.sub(r'[^a-z0-9]+', '', username_base)
    email = f"{first_name.lower()}.{last_name.lower()}{fake.random_int(1, 999)}@example.com"
    
    admin_data = {
        "firstName": first_name,
        "lastName": last_name,
        "username": username,
        "plainPassword": "123456",
        "email": email,
    }
    
    if not required_only:
        admin_data["enabled"] = True
        admin_data["localeCode"] = "es_ES"
    
    return admin_data