from rest_framework import serializers

from footboll_field.models import FootballField
from users.serializers import UserSerializer


class FootballFieldSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = FootballField
        fields = ('owner','name', 'address', 'description', 'image', 'price_per_hour', 'status')
        read_only_fields = ('id', 'created_at', 'updated_at', 'owner')

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['owner'] = request.user
        return super().create(validated_data)
