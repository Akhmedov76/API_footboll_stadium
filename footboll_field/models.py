from django.db import models


class FootballField(models.Model):
    STATUS_CHOICES = [('active', 'Active'),
                      ('inactive', 'Inactive')
                      ]
    name = models.CharField(max_length=100)
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='fields')
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
    bookings = models.ManyToManyField('Booking', related_name='football_fields')
    bookings_total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Football Field'
        verbose_name_plural = 'Football Fields'
        ordering = ['name']
