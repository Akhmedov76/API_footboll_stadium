import os
import random

import django
from django.contrib.auth.hashers import make_password
from django.db import connection
from faker import Faker

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")
django.setup()

fake = Faker("uz_UZ")


def generate_uzbekistan_users(count=50):
    users = []
    address = f"{fake.street_address()}, {fake.city()}, Oʻzbekiston"
    for _ in range(count):
        username = fake.user_name()
        password = make_password("password123")
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        role = "manager"
        phone = f"+998{random.randint(90, 99)}{random.randint(1000000, 9999999)}"
        address = address
        status_user = "active"
        is_superuser = False
        is_active = True
        is_staff = False

        latitude = round(random.uniform(37.18, 45.6), 6)
        longitude = round(random.uniform(58.00, 71.0), 6)

        users.append([
            username, password, first_name, last_name, email, role, phone, address, status_user,
            latitude, longitude, is_superuser, is_active, is_staff
        ])

    with connection.cursor() as cursor:
        cursor.executemany("""
            INSERT INTO users_user 
            (username, password, first_name, last_name, email, role, phone, address, status, latitude, longitude, is_superuser, is_active, is_staff, date_joined)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
        """, users)

    print(f"✅ {count} user created")


if __name__ == "__main__":
    generate_uzbekistan_users(50)
