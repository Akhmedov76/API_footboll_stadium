from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    """

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role', 'phone', 'address')
        read_only_fields = ('role',)


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user.
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'phone', 'address', 'latitude', 'longitude')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
