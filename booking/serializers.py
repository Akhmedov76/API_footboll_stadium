from rest_framework import serializers

from booking.models import Booking
from footboll_field.serializers import FootballFieldSerializer
from footboll_stadium.serializers import FootballStadiumSerializer
from users.serializers import UserSerializer


class BookingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    field = FootballFieldSerializer(read_only=True)
    start_time = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S")
    end_time = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S")

    class Meta:
        model = Booking
        fields = ('id', 'field', 'user', 'start_time', 'end_time', 'status',)
        read_only_fields = ('id', 'created_at', 'updated_at', 'user')

    def validate(self, data):
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError("End time must be after start time")
