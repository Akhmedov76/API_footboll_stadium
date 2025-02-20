from booking.models import Booking
from footboll_field.models import FootballField


def get_available_fields(start_time, end_time):
    booked_fields = Booking.objects.filter(
        status="confirmed",
        start_time__lt=end_time,
        end_time__gt=start_time
    ).values_list("field_id", flat=True)

    available_fields = FootballField.objects.exclude(id__in=booked_fields)
    return available_fields
