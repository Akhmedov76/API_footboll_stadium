from rest_framework import serializers

from booking.models import Booking
from footboll_stadium.serializers import FootballStadiumSerializer
from users.serializers import UserSerializer


class BookingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    field = FootballStadiumSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = ('id', 'field', 'user', 'start_time', 'end_time', 'status',)
        read_only_fields = ('id', 'created_at', 'updated_at', 'user')

    def validate(self, data):
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError("End time must be after start time")
