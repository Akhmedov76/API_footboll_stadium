import asyncio

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.geolocations import get_coordinates_from_address


class User(AbstractUser):
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

    # def is_admin(self):
    #     return self.role == 'admin'
    #
    # def is_owner(self):
    #     return self.role == 'manager'

    # def clean(self):
    #     if User.objects.filter(phone=self.phone).exclude(id=self.id).exists():
    #         raise ValidationError("This phone number is already in use.")

    def save(self, *args, **kwargs):
        if self.address:
            coordinates = asyncio.run(get_coordinates_from_address(self.address))
            if coordinates:
                self.latitude, self.longitude = coordinates
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
