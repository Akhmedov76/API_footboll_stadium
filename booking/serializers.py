from rest_framework import serializers

from booking.models import Booking
from footboll_field.serializers import FootballFieldSerializer
from users.serializers import UserSerializer


class BookingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    field = FootballFieldSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'user')

    def validate(self, data):
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError("End time must be after start time")

        overlapping = Booking.objects.filter(
            field=data['field'],
            start_time__lt=data['end_time'],
            end_time__gt=data['start_time'],
            status='CONFIRMED'
        ).exists()

        if overlapping:
            raise serializers.ValidationError("This time slot is already booked")

        return data
