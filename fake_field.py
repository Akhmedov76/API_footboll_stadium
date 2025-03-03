import os
import random

import django
from django.utils.timezone import now
from faker import Faker

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")
django.setup()

from footboll_field.models import FootballField

fake = Faker("uz_UZ")


def generate_fake_fields(count=1000):
    field = list(FootballField.objects.filter(status='active'))
    if not field:
        print("Football field not found. Please create football field!!!")
        return

    fields = []
    for _ in range(count):
        fields.append(FootballField(
            name=fake.city(),
            stadium=random.choice(field),
            image=None,
            price_per_hour=random.uniform(50, 100),
            status="active",
            created_at=now(),
            updated_at=now(),
            working_hours_start="09:00",
            working_hours_end="18:00"
        ))

    FootballField.objects.bulk_create(fields)
    print(f"�� {len(fields)} football field created")


if __name__ == "__main__":
    generate_fake_fields(1000)
