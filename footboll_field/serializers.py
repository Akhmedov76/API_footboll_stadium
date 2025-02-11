from rest_framework import serializers

from footboll_field.models import FootballField
from users.serializers import UserSerializer


class FootballFieldSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = FootballField
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'owner')
