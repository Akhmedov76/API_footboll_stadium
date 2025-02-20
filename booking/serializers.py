from django.utils.timezone import now
from rest_framework import serializers
from booking.models import Booking
from footboll_field.models import FootballField


class BookingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    field = serializers.PrimaryKeyRelatedField(queryset=FootballField.objects.all())
    start_time = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S", input_formats=["%d.%m.%Y %H:%M:%S"])
    end_time = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S", input_formats=["%d.%m.%Y %H:%M:%S"])

    class Meta:
        model = Booking
        fields = ('id', 'field', 'user', 'start_time', 'end_time', 'status',)
        read_only_fields = ('id', 'created_at', 'updated_at', 'user')

    def validate(self, data):
        start_time = data['start_time']
        end_time = data['end_time']
        field = data['field']

        if start_time >= end_time:
            raise serializers.ValidationError("End time must be after start time")

        existing_booking = Booking.objects.filter(
            field=field,
            status="confirmed",
            start_time__lt=end_time,
            end_time__gt=start_time
        ).exists()

        if existing_booking:
            raise serializers.ValidationError("This field is already booked for the selected time range.")

        return data
