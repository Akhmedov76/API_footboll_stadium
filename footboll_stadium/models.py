import asyncio
from math import cos, radians

from django.db import models

from users.models import User
from utils.geolocations import get_coordinates_from_address


class FootballField(models.Model):
    STATUS_CHOICES = [('active', 'Active'),
                      ('inactive', 'Inactive')
                      ]
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fields')
    address = models.TextField()
    contact = models.CharField(max_length=250, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='stadium/', blank=True, null=True)
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.address:
            coordinates = asyncio.run(get_coordinates_from_address(self.address))
            if coordinates:
                self.latitude, self.longitude = coordinates
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Football Field'
        verbose_name_plural = 'Football Fields'
        ordering = ['name']
