from rest_framework import serializers

from footboll_stadium.models import FootballStadium
from users.serializers import UserSerializer


class FootballStadiumSerializer(serializers.ModelSerializer):
    """
    Serializer for FootballStadium model.
    """
    owner = UserSerializer(read_only=True)

    class Meta:
        model = FootballStadium
        fields = ('id', 'owner', 'name', 'address', 'description', 'image', 'status')
        read_only_fields = ('id', 'created_at', 'updated_at', 'owner')

    def create(self, validated_data):
        request = self.context.get('request')
        if not request.user.is_staff and request.user.role != "manager":
            raise serializers.ValidationError("Authentication information was not provided!")

        validated_data['owner'] = request.user
        return super().create(validated_data)
