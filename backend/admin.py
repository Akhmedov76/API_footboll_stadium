import asyncio

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from utils.geolocations import get_coordinates_from_address


def sync_get_coordinates(address):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(get_coordinates_from_address(address))


class User(AbstractUser):
    ROLES = (
        ('admin', 'Admin'),
        ('OWNER', 'Field Owner'),
        ('user', 'User'),
    )

    role = models.CharField(max_length=10, choices=ROLES, default='user')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active')

    def save(self, *args, **kwargs):
        if self.address:
            coordinates = sync_get_coordinates(self.address)
            if coordinates:
                self.latitude, self.longitude = coordinates
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class FootballField(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fields')
    address = models.TextField()
    description = models.TextField(blank=True)
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Booking(models.Model):
    field = models.ForeignKey(FootballField, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('PENDING', 'Pending'),
            ('CONFIRMED', 'Confirmed'),
            ('CANCELLED', 'Cancelled'),
        ],
        default='PENDING'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_time']

    def __str__(self):
        return f"{self.field.name} - {self.start_time}"
