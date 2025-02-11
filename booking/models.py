import asyncio
from django.conf import settings
from django.db import models
from geopy.distance import geodesic
from footboll_field.models import FootballField
from users.models import User
from utils.geolocations import get_coordinates_from_address
from django.utils.translation import gettext_lazy as _


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
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    distance = models.FloatField(help_text=_('Distance in kilometers'), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        if self.latitude is not None and self.longitude is not None:
            rest_location = (
                settings.STADIUM_LOCATION['latitude'],
                settings.STADIUM_LOCATION['longitude']
            )
            client_location = (self.latitude, self.longitude)
            self.distance = geodesic(rest_location, client_location).km
            self.distance = round(self.distance, 2)

        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-start_time']

    def __str__(self):
        return f"{self.field.name} - {self.start_time}"
