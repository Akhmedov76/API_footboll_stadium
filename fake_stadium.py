import os
import random

import django
from django.utils.timezone import now
from faker import Faker

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")
django.setup()

from footboll_stadium.models import FootballStadium
from users.models import User

fake = Faker("uz_UZ")


def generate_fake_stadiums(count=1000):
    users = list(User.objects.filter(role="manager"))
    if not users:
        print("Admin or users not found. Please create admin or users!!!")
        return

    stadiums = []
    for _ in range(count):
        latitude = round(random.uniform(37.18, 45.6), 6)
        longitude = round(random.uniform(58.00, 71.0), 6)

        address = f"{fake.street_address()}, {fake.city()}, Oʻzbekiston"

        stadiums.append(FootballStadium(
            name=fake.city(),
            owner=random.choice(users),
            address=address,
            contact=f"+998{random.randint(90, 99)}{random.randint(1000000, 9999999)}",
            description=fake.text(),
            image=None,
            latitude=latitude,
            longitude=longitude,
            status="active",
            created_at=now(),
            updated_at=now(),
        ))

    FootballStadium.objects.bulk_create(stadiums)
    print(f"✅ {len(stadiums)} stadium created")


if __name__ == "__main__":
    generate_fake_stadiums(1000)
