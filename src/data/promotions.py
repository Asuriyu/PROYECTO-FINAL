from faker import Faker
import random

faker = Faker()

def generate_promotion_data(valid=True):
    if valid:
        return {
            "code": faker.lexify(text="PROMO????"),
            "name": faker.sentence(nb_words=3),
            "description": faker.text(max_nb_chars=100),
            "priority": random.randint(0, 10),
            "exclusive": random.choice([True, False]),
            "usageLimit": random.randint(0, 100),
            "startsAt": faker.date_time_this_year().isoformat(),
            "endsAt": faker.date_time_between(start_date="+1d", end_date="+30d").isoformat(),
            "couponBased": random.choice([True, False]),
            "appliesToDiscounted": random.choice([True, False]),
            "channels": ["https://demo.sylius.com/api/v2/shop/channels/FASHION_WEB"]
        }
    else:
        return {
            "code": "",
            "name": None,
            "description": "",
            "priority": "high",
            "exclusive": "yes",
            "usageLimit": -5,
            "startsAt": "invalid_date",
            "endsAt": "invalid_date",
            "couponBased": "no",
            "appliesToDiscounted": None,
            "channels": []
        }