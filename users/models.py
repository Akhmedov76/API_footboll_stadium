import asyncio

from django.contrib.auth.models import AbstractUser
from django.db import models

from utils.geolocations import get_coordinates_from_address


class User(AbstractUser):
    """
        Custom user model for stadium booking application.
    """
    ROLES = (
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=10, choices=ROLES, default='user')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active')

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        """
        Get latitude and longitude from address when saving a user.
        """
        if self.address:
            coordinates = asyncio.run(get_coordinates_from_address(self.address))
            print(coordinates)
            if coordinates:
                self.latitude, self.longitude = coordinates
        super().save(*args, **kwargs)
