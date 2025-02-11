from rest_framework import serializers
from .models import User, FootballField, Booking


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'role', 'address', 'phone', 'latitude', 'longitude')
        read_only_fields = ('role',)


class FootballFieldSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = FootballField
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'owner')


class BookingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    field = FootballFieldSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'user')

    def validate(self, data):
        # Serves to check all cases
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


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'phone', 'address', 'latitude', 'longitude')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
