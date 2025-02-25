from rest_framework import serializers

from users.serializers import UserSerializer
from .models import FootballField


class FootballFieldSerializer(serializers.ModelSerializer):
    """
    Serializer for FootballField model.
    """
    user = UserSerializer(read_only=True)

    class Meta:
        model = FootballField
        fields = (
            'id', 'name', 'stadium', 'image', 'price_per_hour', 'status', 'user', 'working_hours_start',
            'working_hours_end')
        read_only_fields = ('id', 'created_at', 'updated_at', 'user')
