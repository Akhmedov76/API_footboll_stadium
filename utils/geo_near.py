from django.db.models import F
from django.db.models.functions import ACos, Cos, Radians, Sin
from django.db.models import FloatField
from footboll_field.models import FootballField


def get_nearest_fields(user_lat, user_lon):
    fields = FootballField.objects.annotate(
        distance=ACos(
            Cos(Radians(user_lat)) * Cos(Radians(F('latitude'))) *
            Cos(Radians(F('longitude')) - Radians(user_lon)) +
            Sin(Radians(user_lat)) * Sin(Radians(F('latitude')))
        ) * 6371
    ).order_by('distance')

    return fields
