import asyncio

from django.db import models
from django.utils.timezone import now

from users.models import User
from utils.geolocations import get_coordinates_from_address


class FootballStadium(models.Model):
    """
        Football stadium model for users.
    """
    STATUS_CHOICES = [('active', 'Active'),
                      ('inactive', 'Inactive')
                      ]
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stadium')
    address = models.TextField()
    contact = models.CharField(max_length=250, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='stadium/', blank=True, null=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.date_joined = now().strftime("%Y-%m-%d %H:%M:%S")
        if self.address:
            coordinates = asyncio.run(get_coordinates_from_address(self.address))
            if coordinates:
                self.latitude, self.longitude = coordinates
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Stadium'
        verbose_name_plural = 'Stadiums'
        ordering = ['name']
