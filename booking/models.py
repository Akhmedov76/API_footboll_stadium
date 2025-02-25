from django.db import models

from footboll_field.models import FootballField
from users.models import User


class Booking(models.Model):
    """
        Booking model for stadiums and fields.
    """
    STATUS_CHOICES = [('pending', 'Pending'),
                      ('confirmed', 'Confirmed'),
                      ('cancelled', 'Cancelled')
                      ]
    field = models.ForeignKey(FootballField, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.field.name} - {self.start_time}"

    class Meta:
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
        ordering = ['-start_time']
