from django.db import models

from footboll_stadium.models import FootballStadium
from users.models import User


class FootballField(models.Model):
    """
        Football field model for stadiums.
    """
    STATUS_CHOICES = [('active', 'Active'),
                      ('inactive', 'Inactive')
                      ]
    name = models.CharField(max_length=100)
    stadium = models.ForeignKey(FootballStadium, on_delete=models.CASCADE, related_name='football_fields')
    image = models.ImageField(upload_to='stadium/', blank=True, null=True)
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    working_hours_start = models.TimeField(default="09:00")
    working_hours_end = models.TimeField(default="18:00")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Football Field'
        verbose_name_plural = 'Football Fields'
        ordering = ['name']
